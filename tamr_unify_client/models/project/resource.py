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
        return self._data.get("name")

    @property
    def external_id(self):
        """:type: str"""
        return self._data.get("externalId")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def type(self):
        """One of:
            ``"SCHEMA_MAPPING"``
            ``"SCHEMA_MAPPING_RECOMMENDATIONS"``
            ``"CATEGORIZATION"``
            ``"DEDUP"``

        :type: str
        """
        return self._data.get("type")

    def unified_dataset(self):
        """Unified dataset for this project.

        :return: Unified dataset for this project.
        :rtype: :class:`~tamr_unify_client.models.dataset.resource.Dataset`
        """
        alias = self.api_path + "/unifiedDataset"
        resource_json = self.client.get(alias).successful().json()
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
        return CategorizationProject(self.client, self._data, self.api_path)

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
        return MasteringProject(self.client, self._data, self.api_path)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r}, "
            f"type={self.type!r})"
        )
