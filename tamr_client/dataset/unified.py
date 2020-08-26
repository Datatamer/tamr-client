"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy

from tamr_client import operation, response
from tamr_client._types import (
    JsonDict,
    Operation,
    Project,
    Session,
    UnifiedDataset,
    URL,
)
from tamr_client.exception import TamrClientException


class NotFound(TamrClientException):
    """Raised when referencing (e.g. updating or deleting) a unified dataset
    that does not exist on the server.
    """

    pass


def from_project(session: Session, project: Project) -> UnifiedDataset:
    """Get unified dataset of a project

    Fetches the unified dataset of a given project from Tamr server

    Args:
        project: Tamr project of this Unified Dataset

    Raises:
        unified.NotFound: If no unified dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = URL(instance=project.url.instance, path=f"{project.url.path}/unifiedDataset")
    return _by_url(session, url)


def _by_url(session: Session, url: URL) -> UnifiedDataset:
    """Get dataset by URL

    Fetches dataset from Tamr server

    Args:
        url: Dataset URL

    Raises:
        unified.NotFound: If no dataset could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> UnifiedDataset:
    """Make unified dataset from JSON data (deserialize)

    Args:
        url: Unified Dataset URL
        data: Unified Dataset JSON data from Tamr server
    """
    cp = deepcopy(data)
    return UnifiedDataset(
        url,
        name=cp["name"],
        description=cp.get("description"),
        key_attribute_names=tuple(cp["keyAttributeNames"]),
    )


def apply_changes(session: Session, unified_dataset: UnifiedDataset) -> Operation:
    """Applies changes to the unified dataset and waits for the operation to complete

    Args:
        unified_dataset: The Unified Dataset which will be committed
    """
    op = _apply_changes_async(session, unified_dataset)
    return operation.wait(session, op)


def _apply_changes_async(
    session: Session, unified_dataset: UnifiedDataset
) -> Operation:
    """Applies changes to the unified dataset

    Args:
        unified_dataset: The Unified Dataset which will be committed
    """
    r = session.post(str(unified_dataset.url) + ":refresh")
    return operation._from_response(unified_dataset.url.instance, r)
