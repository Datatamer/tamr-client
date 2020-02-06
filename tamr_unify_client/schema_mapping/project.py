from tamr_unify_client.project.resource import Project


class SchemaMappingProject(Project):
    """A Schema Mapping project in Tamr."""

    def run(self, refresh_unified_dataset=True):
        """Executes all steps of this project. Ending early if a step fails.

        :param refresh_unified_dataset: Whether refresh should be called on the unified dataset
        :type refresh_unified_dataset: bool
        :rtype: List :class:`~tamr_unify_client.operation.Operation`
        """

        # This list consists of a user defined boolean for whether a task should be done
        # and the function to execute that task
        possible_tasks = [
            (refresh_unified_dataset, self.unified_dataset().refresh)
        ]

        wanted_tasks = [task for should_do, task in possible_tasks if should_do]
        return self._run_subtasks(wanted_tasks)
