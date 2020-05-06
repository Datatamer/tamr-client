from typing import Union

from tamr_client.instance import Instance
from tamr_client.session import Session
from tamr_client.mastering.project import Project as MasteringProject
import tamr_client.response as response
from tamr_client.url import URL
import tamr_client.mastering.project as mastering_project
from tamr_client.types import JsonDict

Project = Union[MasteringProject]


class NotFound(Exception):
    """Raised when referencing (e.g. updating or deleting) a project
    that does not exist on the server."""

    pass


def from_resource_id(session: Session, instance: Instance, id: str) -> Project:
    """Get project by resource ID

    Fetches project from Tamr server

    Args:
        instance: Tamr instance containing this dataset
        id: Project ID

    Raises:
        NotFound: If no project could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = URL(instance=instance, path=f"projects/{id}")
    return _from_url(session, url)


def _from_url(session: Session, url: URL) -> Project:
    """Get project by URL

    Fetches project from Tamr server

    Args:
        url: Project URL

    Raises:
        NotFound: If no project could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> Project:
    """Make project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    proj_type = data["type"]
    if proj_type == "DEDUP":
        return mastering_project._from_json(url, data)
    else:
        raise ValueError(f"Unrecognized project type '{proj_type}' in {repr(data)}")
