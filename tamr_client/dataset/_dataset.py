"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import replace
from typing import Tuple

from tamr_client import operation, response
from tamr_client._types import (
    Attribute,
    Dataset,
    Instance,
    JsonDict,
    Operation,
    Session,
    URL,
)
from tamr_client.attribute import _from_json as _attribute_from_json
from tamr_client.exception import TamrClientException


class NotFound(TamrClientException):
    """Raised when referencing (e.g. updating or deleting) a dataset
    that does not exist on the server.
    """

    pass


class Ambiguous(TamrClientException):
    """Raised when referencing a dataset by name that matches multiple possible targets."""

    pass


def from_resource_id(session: Session, instance: Instance, id: str) -> Dataset:
    """Get dataset by resource ID

    Fetches dataset from Tamr server

    Args:
        instance: Tamr instance containing this dataset
        id: Dataset ID

    Raises:
        dataset.NotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = URL(instance=instance, path=f"datasets/{id}")
    return _from_url(session, url)


def _from_url(session: Session, url: URL) -> Dataset:
    """Get dataset by URL

    Fetches dataset from Tamr server

    Args:
        url: Dataset URL

    Raises:
        dataset.NotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> Dataset:
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


def attributes(session: Session, dataset: Dataset) -> Tuple[Attribute, ...]:
    """Get all attributes from a dataset

    Args:
        dataset: Dataset containing the desired attributes

    Returns:
        The attributes for the specified dataset

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    r = session.get(str(attrs_url))
    attrs_json = response.successful(r).json()

    attrs = []
    for attr_json in attrs_json:
        id = attr_json["name"]
        attr_url = replace(attrs_url, path=attrs_url.path + f"/{id}")
        attr = _attribute_from_json(attr_url, attr_json)
        attrs.append(attr)
    return tuple(attrs)


def refresh(session: Session, dataset: Dataset) -> Operation:
    """Applies changes to the unified dataset and waits for the operation to complete

    Args:
        unified_dataset: The Unified Dataset which will be committed
    """
    op = _refresh_async(session, dataset)
    return operation.wait(session, op)


def _refresh_async(session: Session, dataset: Dataset) -> Operation:
    """Applies changes to the unified dataset

    Args:
        unified_dataset: The Unified Dataset which will be committed
    """
    r = session.post(
        str(dataset.url) + ":refresh",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    return operation._from_response(dataset.url.instance, r)
