"""
Tamr - Categorization
See https://docs.tamr.com/docs/overall-workflow-classification

The terminology used here is consistent with Tamr UI terminology

Asynchronous versions of each function can be found with the suffix `_async` and may be of
interest to power users
"""
from tamr_client import operation
from tamr_client._types import CategorizationProject, Dataset, Operation, Session
from tamr_client.dataset import _dataset, unified


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


def update_unified_dataset(
    session: Session, project: CategorizationProject
) -> Operation:
    """Apply changes to the unified dataset and wait for the operation to complete

    Args:
        project: Tamr Categorization project
    """
    unified_dataset = unified.from_project(session, project)
    op = unified._apply_changes_async(session, unified_dataset)
    return operation.wait(session, op)


def apply_feedback(session: Session, project: CategorizationProject) -> Operation:
    """Train the categorization model according to verified labels and wait for the
    operation to complete

    Args:
        project: Tamr Categorization project
    """
    op = _apply_feedback_async(session, project)
    return operation.wait(session, op)


def update_results(session: Session, project: CategorizationProject) -> Operation:
    """Generate classifications based on the latest categorization model and wait for the
    operation to complete

    Args:
        project: Tamr Categorization project
    """
    op = _update_results_async(session, project)
    return operation.wait(session, op)


def _apply_feedback_async(
    session: Session, project: CategorizationProject
) -> Operation:
    r = session.post(str(project.url) + "/categorizations/model:refresh")
    return operation._from_response(project.url.instance, r)


def _update_results_async(
    session: Session, project: CategorizationProject
) -> Operation:
    r = session.post(str(project.url) + "/categorizations:refresh")
    return operation._from_response(project.url.instance, r)
