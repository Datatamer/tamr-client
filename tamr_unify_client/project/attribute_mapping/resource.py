from copy import deepcopy


class AttributeMapping:
    """see https://docs.tamr.com/reference#retrieve-projects-mappings
    AttributeMapping and AttributeMappingCollection do not inherit from BaseResource and BaseCollection.
    BC and BR require a specific URL for each individual attribute mapping
    (ex: /projects/1/attributeMappings/1), but these types of URLs do not exist for attribute mappings
    """

    def __init__(self, client, data):
        self._data = data
        self.client = client
        # AttributeMapping cannot be aliased, and Project cannot be aliased,
        # so AttributeMapping only ever has one address, which is both
        # its relative_id and its api_path.
        self.api_path = self.relative_id

    @property
    def id(self):
        """:type: str"""
        return self._data["id"]

    @property
    def relative_id(self):
        """:type: str"""
        return self._data["relativeId"]

    @property
    def input_attribute_id(self):
        """:type: str"""
        return self._data["inputAttributeId"]

    @property
    def relative_input_attribute_id(self):
        """:type: str"""
        return self._data["relativeInputAttributeId"]

    @property
    def input_dataset_name(self):
        """:type: str"""
        return self._data["inputDatasetName"]

    @property
    def input_attribute_name(self):
        """:type: str"""
        return self._data["inputAttributeName"]

    @property
    def unified_attribute_id(self):
        """:type: str"""
        return self._data["unifiedAttributeId"]

    @property
    def relative_unified_attribute_id(self):
        """:type: str"""
        return self._data["relativeUnifiedAttributeId"]

    @property
    def unified_dataset_name(self):
        """:type: str"""
        return self._data["unifiedDatasetName"]

    @property
    def unified_attribute_name(self):
        """:type: str"""
        return self._data["unifiedAttributeName"]

    @property
    def resource_id(self):
        """:type: str"""
        spliced = self.relative_id.split("attributeMappings/")[1]
        return spliced

    def spec(self):
        """Returns a spec representation of this attribute mapping.

        :return: The attribute mapping spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec.of(self)

    def delete(self):
        """Delete this attribute mapping.

        :return: HTTP response from the server
        :rtype: :class:`requests.Response`
        """
        response = self.client.delete(self.api_path).successful()
        return response

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"id={self.id!r}, "
            f"relative_id={self.relative_id!r}, "
            f"input_attribute_id={self.input_attribute_id!r}, "
            f"relative_input_attribute_id={self.relative_input_attribute_id!r}, "
            f"input_dataset_name={self.input_dataset_name!r}, "
            f"input_attribute_name={self.input_attribute_name!r}, "
            f"unified_attribute_id={self.unified_attribute_id!r}, "
            f"relative_unified_attribute_id={self.relative_unified_attribute_id!r}, "
            f"unified_dataset_name={self.unified_dataset_name!r}, "
            f"unified_attribute_name={self.unified_attribute_name!r})"
        )


class AttributeMappingSpec:
    """A representation of the server view of an attribute mapping"""

    def __init__(self, data):
        self._data = data

    @staticmethod
    def of(resource):
        """Creates an attribute mapping spec from a attribute mapping.

        :param resource: The existing attribute mapping.
        :type resource: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
        :return: The corresponding attribute mapping spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(deepcopy(resource._data))

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new attribute mapping.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec({})

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_input_attribute_id(self, new_input_attribute_id):
        """Creates a new spec with the same properties, updating the input attribute id.

        :param new_input_attribute_id: The new input attribute id.
        :type new_input_attribute_id: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "inputAttributeId": new_input_attribute_id}
        )

    def with_relative_input_attribute_id(self, new_relative_input_attribute_id):
        """Creates a new spec with the same properties, updating the relative input attribute id.

        :param new_relative_input_attribute_id: The new relative input attribute Id.
        :type new_relative_input_attribute_id: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "relativeInputAttributeId": new_relative_input_attribute_id}
        )

    def with_input_dataset_name(self, new_input_dataset_name):
        """Creates a new spec with the same properties, updating the input dataset name.

        :param new_input_dataset_name: The new input dataset name.
        :type new_input_dataset_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "inputDatasetName": new_input_dataset_name}
        )

    def with_input_attribute_name(self, new_input_attribute_name):
        """Creates a new spec with the same properties, updating the input attribute name.

        :param new_input_attribute_name: The new input attribute name.
        :type new_input_attribute_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "inputAttributeName": new_input_attribute_name}
        )

    def with_unified_attribute_id(self, new_unified_attribute_id):
        """Creates a new spec with the same properties, updating the unified attribute id.

        :param new_unified_attribute_id: The new unified attribute id.
        :type new_unified_attribute_id: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "unifiedAttributeId": new_unified_attribute_id}
        )

    def with_relative_unified_attribute_id(self, new_relative_unified_attribute_id):
        """Creates a new spec with the same properties, updating the relative unified attribute id.

        :param new_relative_unified_attribute_id: The new relative unified attribute id.
        :type new_relative_unified_attribute_id: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {
                **self._data,
                "relativeUnifiedAttributeId": new_relative_unified_attribute_id,
            }
        )

    def with_unified_dataset_name(self, new_unified_dataset_name):
        """Creates a new spec with the same properties, updating the unified dataset name.

        :param new_unified_dataset_name: The new unified dataset name.
        :type new_unified_dataset_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "unifiedDatasetName": new_unified_dataset_name}
        )

    def with_unified_attribute_name(self, new_unified_attribute_name):
        """Creates a new spec with the same properties, updating the unified attribute name.

        :param new_unified_attribute_name: The new unified attribute name.
        :type new_unified_attribute_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMappingSpec`
        """
        return AttributeMappingSpec(
            {**self._data, "unifiedAttributeName": new_unified_attribute_name}
        )

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )
