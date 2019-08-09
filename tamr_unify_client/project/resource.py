import copy

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
        dataset_id = dataset.relative_id.split("/")[-1]
        response = self.client.post(
            self.api_path + "/inputDatasets" + f"?id={dataset_id}"
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

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r}, "
            f"type={self.type!r})"
        )


class ProjectBuilder:
    """A builder object to modify an existing project.

    :param project: The project to modify.
    :type project: :class:`~tamr_unify_client.project.resource.Project`
    """

    def __init__(self, project):
        self._data = copy.deepcopy(project._data)
        self.client = project.client
        self.api_path = project.api_path

    def with_name(self, new_name):
        """Modifies the project's name.

        :param new_name: The updated name.
        :type new_name: str
        :return: This project builder.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectBuilder`
        """
        self._data["name"] = new_name
        return self

    def with_description(self, new_description):
        """Modifies the project's description.

        :param new_description: The updated description.
        :type new_description: str
        :return: This project builder.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectBuilder`
        """
        self._data["description"] = new_description
        return self

    def with_external_id(self, new_external_id):
        """Modifies the project's external ID.

        :param new_external_id: The updated external ID.
        :type new_external_id: str
        :return: This project builder.
        :rtype: :class:`~tamr_unify_client.project.resource.ProjectBuilder`
        """
        self._data["externalId"] = new_external_id
        return self

    def put(self):
        """Commits these changes by updating the project in Unify.

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
            f"relative_id={self._data['relativeId']!r}, "
            f"name={self._data['name']!r}, "
            f"external_id={self._data['externalId']!r}, "
            f"description={self._data['description']!r})"
        )
