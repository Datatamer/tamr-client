"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple

import tamr_client as tc
from tamr_client.types import JsonDict


class DatasetNotFound(Exception):
    """Raised when referencing (e.g. updating or deleting) a dataset
    that does not exist on the server.
    """

    pass


@dataclass(frozen=True)
class Dataset:
    """A Tamr dataset

    See https://docs.tamr.com/reference/dataset-models

    Args:
        url
        key_attribute_names
    """

    url: tc.URL
    name: str
    key_attribute_names: Tuple[str, ...]
    description: Optional[str] = None


def from_resource_id(session: tc.Session, instance: tc.Instance, id: str) -> Dataset:
    """Get dataset by resource ID

    Fetches dataset from Tamr server

    Args:
        instance: Tamr instance containing this dataset
        id: Dataset ID

    Raises:
        DatasetNotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = tc.URL(instance=instance, path=f"datasets/{id}")
    return _from_url(session, url)


def _from_url(session: tc.Session, url: tc.URL) -> Dataset:
    """Get dataset by URL

    Fetches dataset from Tamr server

    Args:
        url: Dataset URL

    Raises:
        DatasetNotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise DatasetNotFound(str(url))
    data = tc.response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: tc.URL, data: JsonDict) -> Dataset:
    """Make dataset from JSON data (deserialize)

    Args:
        url: Dataset URL
        data: Dataset JSON data from Tamr server
    """
    cp = deepcopy(data)
    return Dataset(
        url,
        name=cp["name"],
        description=cp.get("description"),
        key_attribute_names=tuple(cp["keyAttributeNames"]),
    )
