from typing import List, Optional, Tuple, Union

from tamr_client import response
from tamr_client._types import Instance, JsonDict, Project, Session, UnknownProject, URL
from tamr_client.categorization import project as categorization_project
from tamr_client.exception import TamrClientException
from tamr_client.golden_records import project as golden_records_project
from tamr_client.mastering import project as mastering_project
from tamr_client.schema_mapping import project as schema_mapping_project


class NotFound(TamrClientException):
    """Raised when referencing (e.g. updating or deleting) a project
    that does not exist on the server."""

    pass


class Ambiguous(TamrClientException):
    """Raised when referencing a project by name that matches multiple possible targets."""

    pass


class AlreadyExists(TamrClientException):
    """Raised when a project with these specifications already exists."""

    pass


def by_resource_id(session: Session, instance: Instance, id: str) -> Project:
    """Get project by resource ID.
    Fetches project from Tamr server.

    Args:
        instance: Tamr instance containing this dataset
        id: Project ID

    Raises:
        project.NotFound: If no project could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = URL(instance=instance, path=f"projects/{id}")
    return _by_url(session, url)


def by_name(session: Session, instance: Instance, name: str) -> Project:
    """Get project by name
    Fetches project from Tamr server.

    Args:
        instance: Tamr instance containing this project
        name: Project name

    Raises:
        project.NotFound: If no project could be found with that name.
        project.Ambiguous: If multiple targets match project name.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(
        url=str(URL(instance=instance, path="projects")),
        params={"filter": f"name=={name}"},
    )

    # Check that exactly one project is returned
    matches = r.json()
    if len(matches) == 0:
        raise NotFound(str(r.url))
    if len(matches) > 1:
        raise Ambiguous(str(r.url))

    # Make Project from response
    url = URL(instance=instance, path=matches[0]["relativeId"])
    return _from_json(url=url, data=matches[0])


def _by_url(session: Session, url: URL) -> Project:
    """Get project by URL.
    Fetches project from Tamr server.

    Args:
        url: Project URL

    Raises:
        project.NotFound: If no project could be found at the specified URL.
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
    elif proj_type == "CATEGORIZATION":
        return categorization_project._from_json(url, data)
    elif proj_type == "SCHEMA_MAPPING_RECOMMENDATIONS":
        return schema_mapping_project._from_json(url, data)
    elif proj_type == "GOLDEN_RECORDS":
        return golden_records_project._from_json(url, data)
    else:
        return UnknownProject(
            url, name=data["name"], description=data.get("description")
        )


def _create(
    session: Session,
    instance: Instance,
    name: str,
    project_type: str,
    description: Optional[str] = None,
    external_id: Optional[str] = None,
    unified_dataset_name: Optional[str] = None,
) -> Project:
    """Create a project in Tamr.

    Args:
        instance: Tamr instance
        name: Project name
        project_type: Project type
        description: Project description
        external_id: External ID of the project
        unified_dataset_name: Name of the unified dataset

    Returns:
        Project created in Tamr

    Raises:
        project.AlreadyExists: If a project with these specifications already exists.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    if not unified_dataset_name:
        unified_dataset_name = name + "_unified_dataset"
    data = {
        "name": name,
        "type": project_type,
        "unifiedDatasetName": unified_dataset_name,
        "description": description,
        "externalId": external_id,
    }

    project_url = URL(instance=instance, path="projects")
    r = session.post(url=str(project_url), json=data)

    if r.status_code == 409:
        raise AlreadyExists(r.json()["message"])

    data = response.successful(r).json()
    project_path = data["relativeId"]
    project_url = URL(instance=instance, path=str(project_path))

    return _by_url(session=session, url=project_url)


def get_all(
    session: Session,
    instance: Instance,
    *,
    filter: Optional[Union[str, List[str]]] = None,
) -> Tuple[Project, ...]:
    """Get all projects from an instance

    Args:
        instance: Tamr instance from which to get projects
        filter: Filter expression, e.g. "externalId==wobbly"
            Multiple expressions can be passed as a list

    Returns:
        The projects retrieved from the instance

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    url = URL(instance=instance, path="projects")

    if filter is not None:
        r = session.get(str(url), params={"filter": filter})
    else:
        r = session.get(str(url))

    projects_json = response.successful(r).json()

    projects = []
    for project_json in projects_json:
        project_url = URL(instance=instance, path=project_json["relativeId"])
        project = _from_json(project_url, project_json)
        projects.append(project)
    return tuple(projects)
