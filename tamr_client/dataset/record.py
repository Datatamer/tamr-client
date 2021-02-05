"""
See https://docs.tamr.com/reference/record
"The recommended approach for modifying records is to use the :func:`~tamr_client.record.upsert` and
:func:`~tamr_client.record.delete` functions for all use cases they can handle. For more advanced use cases, the
underlying :func:`~tamr_client.record._update` function can be used directly."
"""
import json
from typing import cast, Dict, IO, Iterable, Iterator, Optional

from tamr_client import primary_key
from tamr_client import response
from tamr_client._types import AnyDataset, Dataset, JsonDict, Session


def _update(session: Session, dataset: Dataset, updates: Iterable[Dict]) -> JsonDict:
    """Send a batch of record creations/updates/deletions to this dataset.
    You probably want to use :func:`~tamr_client.record.upsert`
    or :func:`~tamr_client.record.delete` instead.

    Args:
        dataset: Dataset containing records to be updated
        updates: Each update should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
    """
    stringified_updates = (json.dumps(update).encode("utf-8") for update in updates)
    # `requests` accepts a generator for `data` param, but stubs for `requests` in https://github.com/python/typeshed expects this to be a file-like object
    io_updates = cast(IO, stringified_updates)
    r = session.post(
        str(dataset.url) + ":updateRecords",
        headers={"Content-Encoding": "utf-8"},
        data=io_updates,
    )
    return response.successful(r).json()


def upsert(
    session: Session,
    dataset: Dataset,
    records: Iterable[Dict],
    *,
    primary_key_name: Optional[str] = None,
) -> JsonDict:
    """Create or update the specified records.

    Args:
        dataset: Dataset to receive record updates
        records: The records to update, as dictionaries
        primary_key_name: The primary key for these records, which must be a key in each record dictionary.
            By default the key_attribute_name of dataset

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        primary_key.NotFound: If primary_key_name does not match dataset primary key
        primary_key.NotFound: If primary_key_name not in a record dictionary
    """
    if primary_key_name is None:
        primary_key_name = dataset.key_attribute_names[0]

    if primary_key_name not in dataset.key_attribute_names:
        raise primary_key.NotFound(
            f"Primary key: {primary_key_name} is not in dataset key attribute names: {dataset.key_attribute_names}"
        )
    updates = (
        _create_command(record, primary_key_name=primary_key_name) for record in records
    )
    return _update(session, dataset, updates)


def delete(
    session: Session,
    dataset: Dataset,
    records: Iterable[Dict],
    *,
    primary_key_name: Optional[str] = None,
) -> JsonDict:
    """Deletes the specified records, based on primary key values.  Does not check that other attribute values match.

    Args:
        dataset: Dataset from which to delete records
        records: The records to update, as dictionaries
        primary_key_name: The primary key for these records, which must be a key in each record dictionary.
            By default the key_attribute_name of dataset

    Returns:
        JSON response body from server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        primary_key.NotFound: If primary_key_name does not match dataset primary key
        primary_key.NotFound: If primary_key_name not in a record dictionary
    """
    if primary_key_name is None:
        primary_key_name = dataset.key_attribute_names[0]

    if primary_key_name not in dataset.key_attribute_names:
        raise primary_key.NotFound(
            f"Primary key: {primary_key_name} is not in dataset key attribute names: {dataset.key_attribute_names}"
        )
    updates = (
        _delete_command(record, primary_key_name=primary_key_name) for record in records
    )
    return _update(session, dataset, updates)


def _create_command(record: Dict, *, primary_key_name: str) -> Dict:
    """Generates the CREATE command formatted as specified in the `Public Docs for Dataset updates
    <https://docs.tamr.com/reference#modify-a-datasets-records>`_.

    Args:
        record: The record to create, as a dictionary
        primary_key_name: The primary key for this record, which must be a key in the dictionary

    Returns:
        The CREATE command in the proper format
    """
    return {"action": "CREATE", "recordId": record[primary_key_name], "record": record}


def _delete_command(record: Dict, *, primary_key_name: str) -> Dict:
    """Generates the DELETE command formatted as specified in the `Public Docs for Dataset updates
    <https://docs.tamr.com/reference#modify-a-datasets-records>`_.

    Args:
        record: The record to delete, as a dictionary
        primary_key_name: The primary key for this record, which must be a key in the dictionary

    Returns:
        The DELETE command in the proper format
    """
    return {"action": "DELETE", "recordId": record[primary_key_name]}


def stream(session: Session, dataset: AnyDataset) -> Iterator[JsonDict]:
    """Stream the records in this dataset as Python dictionaries.

    Args:
        dataset: Dataset from which to stream records

    Returns:
        Python generator yielding records
    """
    with session.get(str(dataset.url) + "/records", stream=True) as r:
        yield from response.ndjson(r)


def delete_all(session: Session, dataset: AnyDataset):
    """Delete all records in this dataset

    Args:
        dataset: Dataset from which to delete records
    """
    r = session.delete(str(dataset.url) + "/records")
    response.successful(r)
