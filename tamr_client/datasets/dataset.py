"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import dataclass, replace
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
    version: str
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
        version = cp["version"],
    )


def attributes(session: tc.Session, dataset: Dataset) -> Tuple["tc.Attribute", ...]:
    """Get attributes for this dataset

    Args:
        dataset: Dataset containing the desired attributes

    Returns:
        The attributes for the specified dataset

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    r = session.get(str(attrs_url))
    attrs_json = tc.response.successful(r).json()

    attrs = []
    for attr_json in attrs_json:
        id = attr_json["name"]
        attr_url = replace(attrs_url, path=attrs_url.path + f"/{id}")
        attr = tc.attribute._from_json(attr_url, attr_json)
        attrs.append(attr)
    return tuple(attrs)
