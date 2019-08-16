from copy import deepcopy

from tamr_unify_client.base_resource import BaseResource
from tamr_unify_client.dataset.collection import DatasetCollection
from tamr_unify_client.dataset.resource import Dataset
from tamr_unify_client.project.attribute_configuration.collection import (
    AttributeConfigurationCollection,
)
from tamr_unify_client.project.attribute_mapping.collection import (
    AttributeMappingCollection,
)


class Project(BaseResource):
    """A Tamr project."""

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
        """A Tamr project type, listed in https://docs.tamr.com/reference#create-a-project.

        :type: str
        """
        return self._data.get("type")

    @property
    def attributes(self):
        """Attributes of this project.

        :return: Attributes of this project.
        :rtype: :class:`~tamr_unify_client.attribute.collection.AttributeCollection`
        """
        from tamr_unify_client.attribute.collection import AttributeCollection

        alias = self.api_path + "/attributes"
        return AttributeCollection(self.client, alias)

    def unified_dataset(self):
        """Unified dataset for this project.

        :return: Unified dataset for this project.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        alias = self.api_path + "/unifiedDataset"
        resource_json = self.client.get(alias).successful().json()
        return Dataset.from_json(self.client, resource_json, alias)

    def as_categorization(self):
        """Convert this project to a :class:`~tamr_unify_client.categorization.project.CategorizationProject`

        :return: This project.
        :rtype: :class:`~tamr_unify_client.categorization.project.CategorizationProject`
        :raises TypeError: If the :attr:`~tamr_unify_client.project.resource.Project.type` of this project is not ``"CATEGORIZATION"``
        """
        from tamr_unify_client.categorization.project import CategorizationProject

        if self.type != "CATEGORIZATION":
            raise TypeError(
                f"Cannot convert project to categorization project. Project type: {self.type}"
            )
        return CategorizationProject(self.client, self._data, self.api_path)

    def as_mastering(self):
        """Convert this project to a :class:`~tamr_unify_client.mastering.project.MasteringProject`

        :return: This project.
        :rtype: :class:`~tamr_unify_client.mastering.project.MasteringProject`
        :raises TypeError: If the :attr:`~tamr_unify_client.project.resource.Project.type` of this project is not ``"DEDUP"``
        """
        from tamr_unify_client.mastering.project import MasteringProject

        if self.type != "DEDUP":
            raise TypeError(
                f"Cannot convert project to mastering project. Project type: {self.type}"
            )
        return MasteringProject(self.client, self._data, self.api_path)

    def add_input_dataset(self, dataset):
        """
        Associate a dataset with a project in Tamr.

        By default, datasets are not associated with any projects.
        They need to be added as input to a project before they can be used
        as part of that project

        :param dataset: The dataset to associate with the project.
        :type dataset: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :return: HTTP response from the server
        :rtype: :class:`requests.Response`
        """
        params = {"id": dataset.relative_id}
        response = self.client.post(
            self.api_path + "/inputDatasets", params=params
        ).successful()
        return response

    def remove_input_dataset(self, dataset):
        """Remove a dataset from a project.

        :param dataset: The dataset to be removed from this project.
        :type dataset: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :return: HTTP response from the server
        :rtype: :class:`requests.Response`
        """
        params = {"id": dataset.relative_id}
        response = self.client.delete(
            self.api_path + "/inputDatasets", params=params
        ).successful()
        return response

    def input_datasets(self):
        """Retrieve a collection of this project's input datasets.

        :return: The project's input datasets.
        :rtype: :class:`~tamr_unify_client.dataset.collection.DatasetCollection`
        """
        alias = self.api_path + "/inputDatasets"
        return DatasetCollection(self.client, alias)

    def attribute_configurations(self):
        """Project's attribute's configurations.

        :returns: The configurations of the attributes of a project.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.collection.AttributeConfigurationCollection`
        """
        alias = self.api_path + "/attributeConfigurations"
        info = AttributeConfigurationCollection(self.client, api_path=alias)
        return info

    def attribute_mappings(self):
        """Project's attribute's mappings.

       :returns: The attribute mappings of a project.
       :rtype: :class:`~tamr_unify_client.project.attribute_mapping.collection.AttributeMappingCollection`
       """
        alias = self.api_path + "/attributeMappings"
        info = AttributeMappingCollection(self.client, alias)
        return info

    def spec(self):
        """Returns this project's spec.

        :return: The spec for the project.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return ProjectSpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r}, "
            f"type={self.type!r})"
        )


class ProjectSpec:
    """A representation of the server view of a project."""

    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates a project spec from a project.

        :param resource: The existing project.
        :type resource: :class:`~tamr_unify_client.project.resource.Project`
        :return: The corresponding project spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return ProjectSpec(resource.client, deepcopy(resource._data), resource.api_path)

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new project.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return ProjectSpec(None, {}, None)

    def from_data(self, data):
        """Creates a spec with the same client and API path as this one, but new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return ProjectSpec(self.client, data, self.api_path)

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_name(self, new_name):
        """Creates a new spec with the same properties, updating name.

        :param new_name: The new name.
        :type new_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return self.from_data({**self._data, "name": new_name})

    def with_description(self, new_description):
        """Creates a new spec with the same properties, updating description.

        :param new_description: The new description.
        :type new_description: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return self.from_data({**self._data, "description": new_description})

    def with_type(self, new_type):
        """Creates a new spec with the same properties, updating type.

        :param new_type: The new type.
        :type new_type: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return self.from_data({**self._data, "type": new_type})

    def with_external_id(self, new_external_id):
        """Creates a new spec with the same properties, updating external ID.

        :param new_external_id: The new external ID.
        :type new_external_id: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return self.from_data({**self._data, "externalId": new_external_id})

    def with_unified_dataset_name(self, new_unified_dataset_name):
        """Creates a new spec with the same properties, updating unified dataset name.

        :param new_unified_dataset_name: The new unified dataset name.
        :type new_unified_dataset_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectSpec`
        """
        return self.from_data(
            {**self._data, "unifiedDatasetName": new_unified_dataset_name}
        )

    def put(self):
        """Commits these changes by updating the project in Tamr.

        :return: The updated project.
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        """
        updated_json = (
            self.client.put(self.api_path, json=self._data).successful().json()
        )
        return Project.from_json(self.client, updated_json, self.api_path)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )
