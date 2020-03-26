"""
Convenient functionality for interacting with pandas DataFrames.
"""

import json

import pandas as pd

import tamr_client as tc
from tamr_client.types import JsonDict


def upsert(
    session: tc.Session, dataset: tc.Dataset, df: pd.DataFrame, *, primary_key_name: str
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
        raise tc.PrimaryKeyNotFound(
            f"Primary key: {primary_key_name} is not in DataFrame column names: {df.columns}"
        )
    # serialize records via to_json to handle `np.nan` values
    serialized_records = (x[1].to_json() for x in df.iterrows())
    records = (json.loads(x) for x in serialized_records)
    return tc.datasets.record.upsert(
        session, dataset, records, primary_key_name=primary_key_name
    )
