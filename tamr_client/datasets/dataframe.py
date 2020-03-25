"""
Convenient functionality for interacting with pandas DataFrames.
"""

import json

import pandas as pd

import tamr_client as tc
from tamr_client.datasets.dataset import Dataset
from tamr_client.datasets.record import PrimaryKeyNotFound, upsert
from tamr_client.types import JsonDict


def upsert_from_dataframe(
    session: tc.Session, dataset: Dataset, df: pd.DataFrame, *, primary_key_name: str
) -> JsonDict:
    """Upserts a record for each row of `df` with attributes for each column in `df`.
    Args:
        dataset: Dataset to receive record updates
        df: The DataFrame containing records to be upserted
        primary_key_name: The primary key of the dataset.  Must be a column of `df`.

    Returns:
            JSON response body from the server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        PrimaryKeyNotFound: If `primary_key_name` is not a column in `df`.
    """
    if primary_key_name not in df.columns:
        raise PrimaryKeyNotFound(
            f"Primary key: {primary_key_name} is not in DataFrame column names: {df.columns}"
        )
    records = json.loads(df.to_json(orient="records"))
    return upsert(session, dataset, records, primary_key_name=primary_key_name)
