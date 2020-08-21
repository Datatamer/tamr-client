from typing import Optional

from tamr_client import project
from tamr_client._types import (
    CategorizationProject,
    Dataset,
    Instance,
    JsonDict,
    Project,
    Session,
    URL,
)
from tamr_client.dataset import _dataset, unified


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
        attribute.AlreadyExists: If a project with these specifications already exists
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


def manual_labels(session: Session, project: CategorizationProject) -> Dataset:
    """Get manual labels from a Categorization project.

    Args:
        project: Tamr project containing labels

    Returns:
        Dataset containing manual labels

    Raises:
        dataset.NotFound: If no dataset could be found at the specified URL
        dataset.Ambiguous: If multiple targets match dataset name
    """
    unified_dataset = unified.from_project(session=session, project=project)
    labels_dataset_name = unified_dataset.name + "_manual_categorizations"
    return _dataset.by_name(
        session=session, instance=project.url.instance, name=labels_dataset_name
    )
