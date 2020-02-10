from tamr_unify_client.base_model import MachineLearningModel
from tamr_unify_client.categorization.taxonomy import Taxonomy
from tamr_unify_client.project.resource import Project


class CategorizationProject(Project):
    """A Categorization project in Tamr."""

    def model(self):
        """Machine learning model for this Categorization project.
        Learns from verified labels and predicts categorization labels for unlabeled records.

        :returns: The machine learning model for categorization.
        :rtype: :class:`~tamr_unify_client.base_model.MachineLearningModel`
        """
        alias = self.api_path + "/categorizations/model"
        return MachineLearningModel(self.client, None, alias)

    def create_taxonomy(self, creation_spec):
        """Creates a :class:`~tamr_unify_client.categorization.taxonomy.Taxonomy` for this project.

        A taxonomy cannot already be associated with this project.

        :param creation_spec: The creation specification for the taxonomy, which can include name.
        :type creation_spec: dict
        :returns: The new Taxonomy
        :rtype: :class:`~tamr_unify_client.categorization.taxonomy.Taxonomy`
        """
        alias = self.api_path + "/taxonomy"
        resource_json = self.client.post(alias, json=creation_spec).successful().json()
        return Taxonomy.from_json(self.client, resource_json, alias)

    def taxonomy(self):
        """Retrieves the :class:`~tamr_unify_client.categorization.taxonomy.Taxonomy` associated with this project.
        If a taxonomy is not already associated with this project,
        call :func:`~tamr_unify_client.categorization.project.CategorizationProject.create_taxonomy` first.

        :returns: The project's Taxonomy
        :rtype: :class:`~tamr_unify_client.categorization.taxonomy.Taxonomy`
        """
        alias = self.api_path + "/taxonomy"
        resource_json = self.client.get(alias).successful().json()
        return Taxonomy.from_json(self.client, resource_json, alias)

    def run(self, *, refresh_unified_dataset=True, train_model=True, predict_model=True):
        """Executes all steps of this project.

        :param refresh_unified_dataset: Whether refresh should be called on the unified dataset
        :type refresh_unified_dataset: bool
        :param train_model: Whether train should be called on the pair matching model
        :type train_model: bool
        :param predict_model: Whether predict should be called on the pair matching model
        :type predict_model: bool
        :return: Responses from the operations that were run
        :rtype: List :class:`~tamr_unify_client.operation.Operation`
        """

        completed_operations = []
        if refresh_unified_dataset:
            op = self.unified_dataset().refresh()
            if not op.succeeded():
                raise RuntimeError(f"Operation failed: {op}. Completed operations: {completed_operations}")
            else:
                completed_operations.append(op)
        if train_model:
            op = self.model().train()
            if not op.succeeded():
                raise RuntimeError(f"Operation failed: {op}. Completed operations: {completed_operations}")
            else:
                completed_operations.append(op)
        if predict_model:
            op = self.model().predict()
            if not op.succeeded():
                raise RuntimeError(f"Operation failed: {op}. Completed operations: {completed_operations}")
            else:
                completed_operations.append(op)

        return completed_operations

    # super.__repr__ is sufficient
