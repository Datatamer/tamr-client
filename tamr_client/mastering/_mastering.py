from tamr_client import operation
from tamr_client._types import MasteringProject, Operation, Session
from tamr_client.dataset import unified


def update_unified_dataset(session: Session, project: MasteringProject) -> Operation:
    """Applies changes to the unified dataset and waits for the operation to complete

    Args:
        project: Tamr Mastering project
    """
    unified_dataset = unified.from_project(session, project.url.instance, project)
    return unified.apply_changes(session, unified_dataset)


def estimate_pairs(session: Session, project: MasteringProject) -> Operation:
    """Updates the estimated pair counts

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "estimatedPairCounts:refresh")
    return operation._from_response(project.url.instance, r)


def generate_pairs(session: Session, project: MasteringProject) -> Operation:
    """Generates pairs according to the binning model

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "recordPairs:refresh")
    return operation._from_response(project.url.instance, r)


def apply_feedback(session: Session, project: MasteringProject) -> Operation:
    """Trains the pair-matching model according to verified labels

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "recordPairsWithPredictions/model:refresh")
    return operation._from_response(project.url.instance, r)


def update_pair_results(session: Session, project: MasteringProject) -> Operation:
    """Update record pair predictions according to the latest pair-matching model

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "recordPairsWithPredictions:refresh")
    return operation._from_response(project.url.instance, r)


def update_high_impact_pairs(session: Session, project: MasteringProject) -> Operation:
    """Produces new high-impact pairs according to the latest pair-matching model

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "highImpactPairs:refresh")
    return operation._from_response(project.url.instance, r)


def update_cluster_results(session: Session, project: MasteringProject) -> Operation:
    """Generates clusters based on the latest pair-matching model

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "recordClusters:refresh")
    return operation._from_response(project.url.instance, r)


def publish_clusters(session: Session, project: MasteringProject) -> Operation:
    """Publishes current record clusters

    Args:
        project: Tamr Mastering project
    """
    r = session.post(str(project.url) + "publishedClustersWithData:refresh")
    return operation._from_response(project.url.instance, r)
