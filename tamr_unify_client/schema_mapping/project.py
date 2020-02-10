from tamr_unify_client.project.resource import Project


class SchemaMappingProject(Project):
    """A Schema Mapping project in Tamr."""

    def run(self, *, refresh_unified_dataset=True):
        """Executes all steps of this project.

        :param refresh_unified_dataset: Whether refresh should be called on the unified dataset
        :type refresh_unified_dataset: bool
        :rtype: List :class:`~tamr_unify_client.operation.Operation`
        """

        completed_operations = []
        if refresh_unified_dataset:
            op = self.unified_dataset().refresh()
            if not op.succeeded():
                raise RuntimeError(f"Operation failed: {op}. Completed operations: {completed_operations}")
            else:
                completed_operations.append(op)
        return completed_operations
