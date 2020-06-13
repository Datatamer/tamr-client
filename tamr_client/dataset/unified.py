"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple

from tamr_client import response
from tamr_client.instance import Instance
from tamr_client.session import Session
from tamr_client.types import JsonDict
from tamr_client.project import Project
from tamr_client.url import URL


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

    url: URL
    name: str
    key_attribute_names: Tuple[str, ...]
    description: Optional[str] = None


def from_project(session: Session, instance: Instance, project: Project) -> Dataset:
    """Get unified dataset of a project

    Fetches dataset from Tamr server

    Args:
        instance: Tamr instance containing this dataset
        project: Tamr project of this Unified Dataset

    Raises:
        UnifiedDatasetNotFound: If no unified dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = URL(instance=instance, path=f"{project.url.path}/unifiedDataset")
    return _from_url(session, url)


def _from_url(session: Session, url: URL) -> Dataset:
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
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> Dataset:
    """Make unified dataset from JSON data (deserialize)

    Args:
        url: Unified Dataset URL
        data: Unified Dataset JSON data from Tamr server
    """
    cp = deepcopy(data)
    return Dataset(
        url,
        name=cp["name"],
        description=cp.get("description"),
        key_attribute_names=tuple(cp["keyAttributeNames"]),
    )


def commit(unified_dataset: Dataset, session: Session) -> JsonDict:
    """Commits the Unified Dataset.

    Args:
        unified_dataset: The UnifiedDataset which will be committed
        session: The Tamr Session
    """
    r = session.post(
        str(unified_dataset.url) + ":refresh",
        headers={"Content-Type": "application/json",
                 "Accept": "application/json"}
    )
    return response.successful(r).json()