"""
Tamr - Schema Mapping
See https://docs.tamr.com/new/docs/overall-workflow-schema

The terminology used here is consistent with Tamr UI terminology

Asynchronous versions of each function can be found with the suffix `_async` and may be of
interest to power users
"""
from tamr_client import operation
from tamr_client._types import Operation, SchemaMappingProject, Session
from tamr_client.dataset import unified


def update_unified_dataset(
    session: Session, project: SchemaMappingProject
) -> Operation:
    """Apply changes to the unified dataset and wait for the operation to complete

    Args:
        project: Tamr Schema Mapping project
    """
    op = _update_unified_dataset_async(session, project)
    return operation.wait(session, op)


def _update_unified_dataset_async(
    session: Session, project: SchemaMappingProject
) -> Operation:
    unified_dataset = unified.from_project(session, project)
    return unified._apply_changes_async(session, unified_dataset)
