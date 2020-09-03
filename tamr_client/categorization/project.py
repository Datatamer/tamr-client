from typing import Optional

from tamr_client import project
from tamr_client._types import (
    CategorizationProject,
    Instance,
    JsonDict,
    Project,
    Session,
    URL,
)


def _from_json(url: URL, data: JsonDict) -> CategorizationProject:
    """Make Categorization project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    return CategorizationProject(
        url, name=data["name"], description=data.get("description")
    )


def create(
    session: Session,
    instance: Instance,
    name: str,
    description: Optional[str] = None,
    external_id: Optional[str] = None,
    unified_dataset_name: Optional[str] = None,
) -> Project:
    """Create a Categorization project in Tamr.

    Args:
        instance: Tamr instance
        name: Project name
        description: Project description
        external_id: External ID of the project
        unified_dataset_name: Unified dataset name. If None, will be set to project name + _'unified_dataset'

    Returns:
        Project created in Tamr

    Raises:
        project.AlreadyExists: If a project with these specifications already exists
        requests.HTTPError: If any other HTTP error is encountered
    """
    return project._create(
        session=session,
        instance=instance,
        name=name,
        project_type="CATEGORIZATION",
        description=description,
        external_id=external_id,
        unified_dataset_name=unified_dataset_name,
    )
