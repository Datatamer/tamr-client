"""
Tamr - Mastering
See https://docs.tamr.com/docs/overall-workflow-mastering

The terminology used here is consistent with Tamr UI terminology

Asynchronous versions of each function can be found with the suffix `_async` and may be of
interest to power users
"""
from tamr_client import operation
from tamr_client._types import MasteringProject, Operation, Session
from tamr_client.dataset import unified


def update_unified_dataset(session: Session, project: MasteringProject) -> Operation:
    """Apply changes to the unified dataset and wait for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    unified_dataset = unified.from_project(session, project)
    op = unified._apply_changes_async(session, unified_dataset)
    return operation.wait(session, op)


def estimate_pairs(session: Session, project: MasteringProject) -> Operation:
    """Update the estimated pair counts and wait for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _estimate_pairs_async(session, project)
    return operation.wait(session, op)


def generate_pairs(session: Session, project: MasteringProject) -> Operation:
    """Generate pairs according to the binning model and wait for the operation
    to complete

    Args:
        project: Tamr Mastering project
    """
    op = _generate_pairs_async(session, project)
    return operation.wait(session, op)


def apply_feedback(session: Session, project: MasteringProject) -> Operation:
    """Train the pair-matching model according to verified labels and wait for the
    operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _apply_feedback_async(session, project)
    return operation.wait(session, op)


def update_pair_results(session: Session, project: MasteringProject) -> Operation:
    """Update record pair predictions according to the latest pair-matching model and
    wait for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _update_pair_results_async(session, project)
    return operation.wait(session, op)


def update_high_impact_pairs(session: Session, project: MasteringProject) -> Operation:
    """Produce new high-impact pairs according to the latest pair-matching model and
    wait for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _update_high_impact_pairs_async(session, project)
    return operation.wait(session, op)


def update_cluster_results(session: Session, project: MasteringProject) -> Operation:
    """Generate clusters based on the latest pair-matching model and wait for the
    operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _update_cluster_results_async(session, project)
    return operation.wait(session, op)


def publish_clusters(session: Session, project: MasteringProject) -> Operation:
    """Publish current record clusters and wait for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    op = _publish_clusters_async(session, project)
    return operation.wait(session, op)


def _estimate_pairs_async(session: Session, project: MasteringProject) -> Operation:
    r = session.post(str(project.url) + "/estimatedPairCounts:refresh")
    return operation._from_response(project.url.instance, r)


def _generate_pairs_async(session: Session, project: MasteringProject) -> Operation:
    r = session.post(str(project.url) + "/recordPairs:refresh")
    return operation._from_response(project.url.instance, r)


def _apply_feedback_async(session: Session, project: MasteringProject) -> Operation:
    r = session.post(str(project.url) + "/recordPairsWithPredictions/model:refresh")
    return operation._from_response(project.url.instance, r)


def _update_pair_results_async(
    session: Session, project: MasteringProject
) -> Operation:
    r = session.post(str(project.url) + "/recordPairsWithPredictions:refresh")
    return operation._from_response(project.url.instance, r)


def _update_high_impact_pairs_async(
    session: Session, project: MasteringProject
) -> Operation:
    r = session.post(str(project.url) + "/highImpactPairs:refresh")
    return operation._from_response(project.url.instance, r)


def _update_cluster_results_async(
    session: Session, project: MasteringProject
) -> Operation:
    r = session.post(str(project.url) + "/recordClusters:refresh")
    return operation._from_response(project.url.instance, r)


def _publish_clusters_async(session: Session, project: MasteringProject) -> Operation:
    r = session.post(str(project.url) + "/publishedClustersWithData:refresh")
    return operation._from_response(project.url.instance, r)
