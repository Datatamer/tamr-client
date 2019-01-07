from unify_api_v1.models.project.resource import Project
from unify_api_v1.models.machine_learning_model import MachineLearningModel


class CategorizationProject(Project):
    """A Categorization project in Unify."""

    def model(self):
        """Machine learning model for this Categorization project.
        Learns from verified labels and predicts categorization labels for unlabeled records.

        :returns: The machine learning model for categorization.
        :rtype: :class:`~unify_api_v1.models.machine_learning_model.MachineLearningModel`
        """
        alias = self.api_path + "/categorizations/model"
        return MachineLearningModel(self.client, None, alias)
