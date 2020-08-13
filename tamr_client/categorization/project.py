from tamr_client._types import (
    CategorizationProject,
    Dataset,
    Instance,
    JsonDict,
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


def manual_labels(
    session: Session, instance: Instance, project: CategorizationProject
) -> Dataset:
    """Get manual labels from a Categorization project
    Args:
        instance: Tamr instance containing project
        project: Tamr project containing labels

    Returns:
        Dataset containing manual labels

    Raises:
        _dataset.NotFound: If no dataset could be found at the specified URL
        Ambiguous: If multiple targets match dataset name
    """
    unified_dataset = unified.from_project(
        session=session, instance=instance, project=project
    )
    labels_dataset_name = unified_dataset.name + "_manual_categorizations"
    datasets_url = URL(instance=instance, path="datasets")
    r = session.get(
        url=str(datasets_url), params={"filter": f"name=={labels_dataset_name}"}
    )
    matches = r.json()
    if len(matches) == 0:
        raise _dataset.NotFound(str(r.url))
    if len(matches) > 1:
        raise _dataset.Ambiguous(str(r.url))

    dataset_path = matches[0]["relativeId"]
    dataset_url = URL(instance=instance, path=dataset_path)
    return _dataset._from_url(session=session, url=dataset_url)
