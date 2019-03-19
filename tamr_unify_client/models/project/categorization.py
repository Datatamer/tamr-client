from tamr_unify_client.models.machine_learning_model import MachineLearningModel
from tamr_unify_client.models.project.resource import Project


class CategorizationProject(Project):
    """A Categorization project in Unify."""

    def model(self):
        """Machine learning model for this Categorization project.
        Learns from verified labels and predicts categorization labels for unlabeled records.

        :returns: The machine learning model for categorization.
        :rtype: :class:`~tamr_unify_client.models.machine_learning_model.MachineLearningModel`
        """
        alias = self.api_path + "/categorizations/model"
        return MachineLearningModel(self.client, None, alias)

    # super.__repr__ is sufficient
