"""
Convenient functionality for interacting with pandas DataFrames.
"""

import json
import os
from typing import Optional, TYPE_CHECKING

import requests

from tamr_client import attribute, dataset, primary_key
from tamr_client._types import Dataset, Instance, JsonDict, Session
from tamr_client.dataset import record
from tamr_client.exception import TamrClientException

BUILDING_DOCS = os.environ.get("TAMR_CLIENT_DOCS") == "1"
if TYPE_CHECKING or BUILDING_DOCS:
    import pandas as pd


class CreationFailure(TamrClientException):
    """Raised when a dataset could not be created from a pandas DataFrame
    """

    pass


def upsert(
    session: Session,
    dataset: Dataset,
    df: "pd.DataFrame",
    *,
    primary_key_name: Optional[str] = None,
) -> JsonDict:
    """Upserts a record for each row of `df` with attributes for each column in `df`.

    Args:
        dataset: Dataset to receive record updates
        df: The DataFrame containing records to be upserted
        primary_key_name: The primary key of the dataset.  Must be a column of `df`. By default the
            key_attribute_name of dataset

    Returns:
        JSON response body from the server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        primary_key.NotFound: If `primary_key_name` is not a column in `df` or the index of `df`
        ValueError: If `primary_key_name` matches both a column in `df` and the index of `df`
    """
    if primary_key_name is None:
        primary_key_name = dataset.key_attribute_names[0]

    # preconditions
    _check_primary_key(df, primary_key_name)

    # promote primary key column to index
    if primary_key_name in df.columns:
        df = df.set_index(primary_key_name)

    # serialize records via to_json to handle `np.nan` values
    serialized_records = ((pk, row.to_json()) for pk, row in df.iterrows())
    records = (
        {primary_key_name: pk, **json.loads(row)} for pk, row in serialized_records
    )
    return record.upsert(session, dataset, records, primary_key_name=primary_key_name)


def create(
    session: Session,
    instance: Instance,
    df: "pd.DataFrame",
    *,
    name: str,
    primary_key_name: Optional[str] = None,
    description: Optional[str] = None,
    external_id: Optional[str] = None,
) -> Dataset:
    """Create a dataset in Tamr from the DataFrame `df` and creates a record from each row

    All attributes other than the primary key are created as the default type array(string)

    Args:
        instance: Tamr instance
        df: The DataFrame containing records to be upserted
        name: Dataset name
        primary_key_name: The primary key of the dataset. Must be a column of `df`. By default the
            name of the index of `df`
        description: Dataset description
        external_id: External ID of the dataset

    Returns:
        Dataset created in Tamr

    Raises:
        dataset.AlreadyExists: If a dataset with these specifications already exists.
        requests.HTTPError: If any other HTTP error is encountered.
        primary_key.NotFound: If `primary_key_name` is not a column in `df` or the index of `df`
        ValueError: If `primary_key_name` matches both a column in `df` and the index of `df`
    """
    # preconditions
    if primary_key_name is None:
        if df.index.name is not None:
            primary_key_name = df.index.name
        else:
            raise primary_key.NotFound(
                "No primary key was specified and DataFrame index is unnamed"
            )
    _check_primary_key(df, primary_key_name)

    # dataset creation
    try:
        ds = dataset.create(
            session,
            instance,
            name=name,
            key_attribute_names=(primary_key_name,),
            description=description,
            external_id=external_id,
        )
    except (TamrClientException, requests.HTTPError) as e:
        raise CreationFailure(f"Dataset was not created: {e}")

    # attribute creation
    for col in df.columns:
        if col == primary_key_name:
            # this attribute already exists as a key attribute
            continue
        try:
            attribute.create(session, ds, name=col, is_nullable=True)
        except (TamrClientException, requests.HTTPError) as e:
            _handle_creation_failure(session, ds, f"An attribute was not created: {e}")

    # record creation
    try:
        response = upsert(session, ds, df, primary_key_name=primary_key_name)
        if not response["allCommandsSucceeded"]:
            _handle_creation_failure(session, ds, "Some records had validation errors")
    except (TamrClientException, requests.HTTPError) as e:
        _handle_creation_failure(session, ds, f"Record could not be created: {e}")

    # Get Dataset from server
    return dataset._dataset._by_url(session, ds.url)


def _handle_creation_failure(session: Session, stub_dataset: Dataset, error: str):
    """Attempt to make `dataframe.create` atomic by deleting the created dataset in the event of
    later failure.

    However, this does not guarantee atomicity: if the request to delete the dataset fails, it will
    not retry.

    Args:
        stub_dataset: The created dataset to delete
        error: The error that caused dataset creation to fail
    """
    try:
        dataset.delete(session, stub_dataset)
    except requests.HTTPError:
        raise CreationFailure(
            f"Created dataset did not delete after an earlier error: {error}"
        )
    raise CreationFailure(error)


def _check_primary_key(df: "pd.DataFrame", primary_key_name: str):
    """Check if the primary key name uniquely identifies a column or index of the DataFrame

    Args:
        df: The DataFrame to inspect
        primary_key_name: The index or column name to be used as the primary key

    Raises:
        primary_key.Ambiguous: If the primary key name matches both the index and a column
        primary_key.NotFound: If the primary key name does not match the index or any column
    """
    if primary_key_name in df.columns and primary_key_name == df.index.name:
        raise primary_key.Ambiguous(
            f"Index {primary_key_name} has the same name as column {primary_key_name}"
        )
    elif primary_key_name not in df.columns and primary_key_name != df.index.name:
        raise primary_key.NotFound(
            f"Primary key: {primary_key_name} is not DataFrame index name: {df.index.name} or in"
            f" DataFrame column names: {df.columns}"
        )
