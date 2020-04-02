"""
Convenient functionality for interacting with pandas DataFrames.
"""

import json
from typing import Optional

import pandas as pd

import tamr_client as tc
from tamr_client.types import JsonDict


def upsert(
    session: tc.Session,
    dataset: tc.Dataset,
    df: pd.DataFrame,
    *,
    primary_key_name: Optional[str] = None,
) -> JsonDict:
    """Upserts a record for each row of `df` with attributes for each column in `df`.
    Args:
        dataset: Dataset to receive record updates
        df: The DataFrame containing records to be upserted
        primary_key_name: The primary key of the dataset.  Must be a column of `df`. By default the key_attribute_name of dataset

    Returns:
        JSON response body from the server

    Raises:
        requests.HTTPError: If an HTTP error is encountered
        PrimaryKeyNotFound: If `primary_key_name` is not a column in `df` or the index of `df`
        ValueError: If `primary_key_name` matches both a column in `df` and the index of `df`
    """
    if not primary_key_name:
        primary_key_name = dataset.key_attribute_names[0]

    if primary_key_name in df.columns and primary_key_name == df.index.name:
        raise ValueError(
            f"Index {primary_key_name} has the same name as column {primary_key_name}"
        )

    if primary_key_name not in df.columns:
        # if `df.index.name` is the primary key, create column from `df.index`
        if primary_key_name == df.index.name:
            df.insert(0, df.index.name, df.index)
        else:
            raise tc.PrimaryKeyNotFound(
                f"Primary key: {primary_key_name} is not DataFrame index name: {df.index.name} or in DataFrame column names: {df.columns}"
            )
    # serialize records via to_json to handle `np.nan` values
    serialized_records = (x[1].to_json() for x in df.iterrows())
    records = (json.loads(x) for x in serialized_records)

    response = tc.datasets.record.upsert(
        session, dataset, records, primary_key_name=primary_key_name
    )

    # if index was used as the primary key, drop column that was created
    if primary_key_name == df.index.name:
        df.drop(primary_key_name, axis=1, inplace=True)

    return response
