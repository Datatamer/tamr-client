"""
Tamr - Golden Records
See https://docs.tamr.com/docs/overview-golden-records

The terminology used here is consistent with Tamr UI terminology

Asynchronous versions of each function can be found with the suffix `_async` and may be of
interest to power users
"""
from tamr_client import operation
from tamr_client._types import GoldenRecordsProject, Operation, Session


def update(session: Session, project: GoldenRecordsProject) -> Operation:
    """Update the draft golden records and wait for the operation to complete

    Args:
        project: Tamr Golden Records project
    """
    op = _update_async(session, project)
    return operation.wait(session, op)


def publish(session: Session, project: GoldenRecordsProject) -> Operation:
    """Publish the golden records and wait for the operation to complete

    Args:
        project: Tamr Golden Records project
    """
    op = _publish_async(session, project)
    return operation.wait(session, op)


def _update_async(session: Session, project: GoldenRecordsProject) -> Operation:
    r = session.post(str(project.url) + "/goldenRecords:refresh")
    return operation._from_response(project.url.instance, r)


def _publish_async(session: Session, project: GoldenRecordsProject) -> Operation:
    r = session.post(
        str(project.url) + "/publishedGoldenRecords:refresh",
        params={"validate": "true", "version": "CURRENT"},
    )
    return operation._from_response(project.url.instance, r)
