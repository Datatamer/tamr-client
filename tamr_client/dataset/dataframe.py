"""
Convenient functionality for interacting with pandas DataFrames.
"""

import json
import os
from typing import Optional, TYPE_CHECKING

from tamr_client import primary_key
from tamr_client._types import Dataset, JsonDict, Session
from tamr_client.dataset import record

BUILDING_DOCS = os.environ.get("TAMR_CLIENT_DOCS") == "1"
if TYPE_CHECKING or BUILDING_DOCS:
    import pandas as pd


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
        primary_key_name: The primary key of the dataset.  Must be a column of `df`. By default the key_attribute_name of dataset

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
    if primary_key_name in df.columns and primary_key_name == df.index.name:
        raise primary_key.Ambiguous(
            f"Index {primary_key_name} has the same name as column {primary_key_name}"
        )
    elif primary_key_name not in df.columns and primary_key_name != df.index.name:
        raise primary_key.NotFound(
            f"Primary key: {primary_key_name} is not DataFrame index name: {df.index.name} or in DataFrame column names: {df.columns}"
        )

    # promote primary key column to index
    if primary_key_name in df.columns:
        df = df.set_index(primary_key_name)

    # serialize records via to_json to handle `np.nan` values
    serialized_records = ((pk, row.to_json()) for pk, row in df.iterrows())
    records = (
        {primary_key_name: pk, **json.loads(row)} for pk, row in serialized_records
    )
    return record.upsert(session, dataset, records, primary_key_name=primary_key_name)
