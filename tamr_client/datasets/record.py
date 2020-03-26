"""
See https://docs.tamr.com/reference/record
"The recommended approach for interacting with records is to use the upsert and delete functions for all use cases they
can handle. For more advanced use cases, the underlying _update function can be used directly."
"""
import json
from typing import Dict, Iterable, Union

import tamr_client as tc
from tamr_client.types import JsonDict


class PrimaryKeyNotFound(Exception):
    """Raised when referencing a primary key by name that does not exist."""

    pass


def _update(
    session: tc.Session, dataset: tc.Dataset, updates: Iterable[Dict]
) -> JsonDict:
    """Send a batch of record creations/updates/deletions to this dataset.
    You probably want to use :func:`~tamr_client.dataset.upsert_records`
    or :func:`~tamr_client.dataset.delete_records` instead.

    Args:
        dataset: Dataset containing records to be updated
        updates: Each update should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
    """
    stringified_updates = (json.dumps(update) for update in updates)
    r = session.post(
        str(dataset.url) + ":updateRecords",
        headers={"Content-Encoding": "utf-8"},
        data=stringified_updates,
    )
    return tc.response.successful(r).json()


def upsert(
    session: tc.Session,
    dataset: tc.Dataset,
    records: Iterable[Dict],
    *,
    primary_key_name: str,
) -> JsonDict:
    """Create or update the specified records.

    Args:
        dataset: Dataset to receive record updates
        records: The records to update, as dictionaries
        primary_key_name: The primary key for these records, which must be a key in each record dictionary

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        PrimaryKeyNotFound: If primary_key_name does not match dataset primary key
        PrimaryKeyNotFound: If primary_key_name not in a record dictionary
    """
    if primary_key_name not in dataset.key_attribute_names:
        raise PrimaryKeyNotFound(
            f"Primary key: {primary_key_name} is not in dataset key attribute names: {dataset.key_attribute_names}"
        )
    updates = (
        {"action": "CREATE", "recordId": record[primary_key_name], "record": record}
        for record in records
    )
    return _update(session, dataset, updates)


def _delete_by_id(
    session: tc.Session, dataset: tc.Dataset, record_ids: Iterable[Union[str, int]]
) -> JsonDict:
    """Deletes the specified records.

    Args:
        dataset: Dataset from which to delete records
        record_ids: The IDs of the records to delete_records

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
    """
    updates = ({"action": "DELETE", "recordId": rid} for rid in record_ids)
    return _update(session, dataset, updates)


def delete(
    session: tc.Session,
    dataset: tc.Dataset,
    records: Iterable[Dict],
    *,
    primary_key_name: str,
) -> JsonDict:
    """Deletes the specified records, based on primary key values.  Does not check that other record values match.

    Args:
        dataset: Dateset from which to delete records
        records: The records to update, as dictionaries
        primary_key_name: The primary key for these records, which must be a key in each record dictionary

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        PrimaryKeyNotFound: If primary_key_name does not match dataset primary key
        PrimaryKeyNotFound: If primary_key_name not in a record dictionary
    """
    if primary_key_name not in dataset.key_attribute_names:
        raise PrimaryKeyNotFound(
            f"Primary key: {primary_key_name} is not in dataset key attribute names: {dataset.key_attribute_names}"
        )
    ids = (record[primary_key_name] for record in records)
    return _delete_by_id(session, dataset, ids)
