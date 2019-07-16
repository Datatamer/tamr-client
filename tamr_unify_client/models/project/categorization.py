from tamr_unify_client.models.machine_learning_model import MachineLearningModel
from tamr_unify_client.models.project.resource import Project
from tamr_unify_client.models.taxonomy.resource import Taxonomy


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

    def create_taxonomy(self, creation_spec):
        """Creates a Taxonomy for this Categorization project.

        A taxonomy cannot already be associated with this project.

        :param creation_spec: The creation specification for the taxonomy, which can include name.
        :type: dict
        :returns: The new Taxonomy
        :rtype: :class:`~tamr_unify_client.models.taxonomy.resource.Taxonomy`
        """
        alias = self.api_path + "/taxonomy"
        resource_json = self.client.post(alias, json=creation_spec).successful().json()
        return Taxonomy.from_json(self.client, resource_json, alias)

    def taxonomy(self):
        """Retrieves the Taxonomy associated with Categorization project.

        If a taxonomy is not already associated with this project, call create_taxonomy() first.

        :returns: The project's Taxonomy
        :rtype: :class:`~tamr_unify_client.models.taxonomy.resource.Taxonomy`
        """
        alias = self.api_path + "/taxonomy"
        resource_json = self.client.get(alias).successful().json()
        return Taxonomy.from_json(self.client, resource_json, alias)

    # super.__repr__ is sufficient
