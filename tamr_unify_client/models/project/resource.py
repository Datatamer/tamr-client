from tamr_unify_client.models.base_resource import BaseResource
from tamr_unify_client.models.dataset.resource import Dataset


class Project(BaseResource):
    """A Unify project."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    @property
    def name(self):
        """:type: str"""
        return self.data["name"]

    @property
    def description(self):
        """:type: str"""
        return self.data["description"]

    @property
    def type(self):
        """One of:
            ``"SCHEMA_MAPPING"``
            ``"SCHEMA_MAPPING_RECOMMENDATIONS"``
            ``"CATEGORIZATION"``
            ``"DEDUP"``

        :type: str
        """
        return self.data["type"]

    def unified_dataset(self):
        """Unified dataset for this project.

        :return: Unified dataset for this project.
        :rtype: :class:`~tamr_unify_client.models.dataset.resource.Dataset`
        """
        alias = self.api_path + "/unifiedDataset"
        resource_json = self.client.get_json(alias)
        return Dataset.from_json(self.client, resource_json, alias)

    def as_categorization(self):
        """Convert this project to a :class:`~tamr_unify_client.models.project.categorization.CategorizationProject`

        :return: This project.
        :rtype: :class:`~tamr_unify_client.models.project.categorization.CategorizationProject`
        :raises TypeError: If the :attr:`~tamr_unify_client.models.project.resource.Project.type` of this project is not ``"CATEGORIZATION"``
        """
        from tamr_unify_client.models.project.categorization import (
            CategorizationProject,
        )

        if self.type != "CATEGORIZATION":
            raise TypeError(
                f"Cannot convert project to categorization project. Project type: {self.type}"
            )
        return CategorizationProject(self.client, self.data, self.api_path)

    def as_mastering(self):
        """Convert this project to a :class:`~tamr_unify_client.models.project.mastering.MasteringProject`

        :return: This project.
        :rtype: :class:`~tamr_unify_client.models.project.mastering.MasteringProject`
        :raises TypeError: If the :attr:`~tamr_unify_client.models.project.resource.Project.type` of this project is not ``"DEDUP"``
        """
        from tamr_unify_client.models.project.mastering import MasteringProject

        if self.type != "DEDUP":
            raise TypeError(
                f"Cannot convert project to mastering project. Project type: {self.type}"
            )
        return MasteringProject(self.client, self.data, self.api_path)
