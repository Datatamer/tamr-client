"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import replace
from typing import List, Optional, Tuple, Union

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


class AlreadyExists(TamrClientException):
    """Raised when a dataset with these specifications already exists."""

    pass


def by_resource_id(session: Session, instance: Instance, id: str) -> Dataset:
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
    return _by_url(session, url)


def by_name(session: Session, instance: Instance, name: str) -> Dataset:
    """Get dataset by name

    Fetches dataset from Tamr server

    Args:
        instance: Tamr instance containing this dataset
        name: Dataset name

    Raises:
        dataset.NotFound: If no dataset could be found with that name.
        dataset.Ambiguous: If multiple targets match dataset name.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(
        url=str(URL(instance=instance, path="datasets")),
        params={"filter": f"name=={name}"},
    )

    # Check that exactly one dataset is returned
    matches = r.json()
    if len(matches) == 0:
        raise NotFound(str(r.url))
    if len(matches) > 1:
        raise Ambiguous(str(r.url))

    # Make Dataset from response
    url = URL(instance=instance, path=matches[0]["relativeId"])
    return _from_json(url=url, data=matches[0])


def _by_url(session: Session, url: URL) -> Dataset:
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


def materialize(session: Session, dataset: Dataset) -> Operation:
    """Materialize a dataset and wait for the operation to complete
    Materializing consists of updating the dataset (including records) in persistent storage (HBase) based on upstream changes to data.

    Args:
        dataset: A Tamr dataset which will be materialized
    """
    op = _materialize_async(session, dataset)
    return operation.wait(session, op)


def _materialize_async(session: Session, dataset: Dataset) -> Operation:
    r = session.post(str(dataset.url) + ":refresh",)
    return operation._from_response(dataset.url.instance, r)


def delete(session: Session, dataset: Dataset, *, cascade: bool = False):
    """Deletes an existing dataset

    Sends a deletion request to the Tamr server

    Args:
        dataset: Existing dataset to delete
        cascade: Whether to delete all derived datasets as well

    Raises:
        dataset.NotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.delete(str(dataset.url), params={"cascade": cascade})
    if r.status_code == 404:
        raise NotFound(str(dataset.url))
    response.successful(r)


def get_all(
    session: Session,
    instance: Instance,
    *,
    filter: Optional[Union[str, List[str]]] = None,
) -> Tuple[Dataset, ...]:
    """Get all datasets from an instance

    Args:
        instance: Tamr instance from which to get datasets
        filter: Filter expression, e.g. "externalId==wobbly"
            Multiple expressions can be passed as a list

    Returns:
        The datasets retrieved from the instance

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    url = URL(instance=instance, path="datasets")

    if filter is not None:
        r = session.get(str(url), params={"filter": filter})
    else:
        r = session.get(str(url))

    datasets_json = response.successful(r).json()

    datasets = []
    for dataset_json in datasets_json:
        dataset_url = URL(instance=instance, path=dataset_json["relativeId"])
        dataset = _from_json(dataset_url, dataset_json)
        datasets.append(dataset)
    return tuple(datasets)


def create(
    session: Session,
    instance: Instance,
    *,
    name: str,
    key_attribute_names: Tuple[str, ...],
    description: Optional[str] = None,
    external_id: Optional[str] = None,
) -> Dataset:
    """Create a dataset in Tamr.

    Args:
        instance: Tamr instance
        name: Dataset name
        key_attribute_names: Dataset primary key attribute names
        description: Dataset description
        external_id: External ID of the dataset

    Returns:
        Dataset created in Tamr

    Raises:
        dataset.AlreadyExists: If a dataset with these specifications already exists.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    data = {
        "name": name,
        "keyAttributeNames": key_attribute_names,
        "description": description,
        "externalId": external_id,
    }

    dataset_url = URL(instance=instance, path="datasets")
    r = session.post(url=str(dataset_url), json=data)

    if r.status_code == 400 and "already exists" in r.json()["message"]:
        raise AlreadyExists(r.json()["message"])

    data = response.successful(r).json()
    dataset_path = data["relativeId"]
    dataset_url = URL(instance=instance, path=str(dataset_path))

    return _by_url(session=session, url=dataset_url)
