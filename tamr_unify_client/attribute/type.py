from copy import deepcopy


class AttributeType:
    """
    The type of an :class:`~tamr_unify_client.attribute.resource.Attribute` or :class:`~tamr_unify_client.attribute.subattribute.SubAttribute`.

    See https://docs.tamr.com/reference#attribute-types

    :param data: JSON data representing this type
    :type data: :py:class:`dict`
    """

    def __init__(self, data):
        self._data = data

    @property
    def base_type(self):
        """:type: str"""
        return self._data.get("baseType")

    @property
    def inner_type(self):
        """:type: :class:`~tamr_unify_client.attribute.type.AttributeType`"""
        if "innerType" in self._data:
            return AttributeType(self._data.get("innerType"))
        else:
            return None

    @property
    def attributes(self):
        """:type: list[:class:`~tamr_unify_client.attribute.subattribute.SubAttribute`]"""
        from tamr_unify_client.attribute.subattribute import SubAttribute

        collection_json = self._data.get("attributes")
        return [SubAttribute.from_json(attr) for attr in collection_json]

    def spec(self):
        """Returns a spec representation of this attribute type.

        :return: The attribute type spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        return AttributeTypeSpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"base_type={self.base_type!r})"
        )


class AttributeTypeSpec:
    def __init__(self, data):
        self._data = data

    @staticmethod
    def of(resource):
        """Creates an attribute type spec from an attribute type.

        :param resource: The existing attribute type.
        :type resource: :class:`~tamr_unify_client.attribute.type.AttributeType`
        :return: The corresponding attribute type spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        return AttributeTypeSpec(deepcopy(resource._data))

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new attribute type.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        return AttributeTypeSpec({})

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_base_type(self, new_base_type):
        """Creates a new spec with the same properties, updating the base type.

        :param new_base_type: The new base type.
        :type new_base_type: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        return AttributeTypeSpec({**self._data, "baseType": new_base_type})

    def with_inner_type(self, new_inner_type):
        """Creates a new spec with the same properties, updating the inner type.

        :param new_inner_type: The spec of the new inner type.
        :type new_inner_type: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        inner_spec = new_inner_type.to_dict()
        return AttributeTypeSpec({**self._data, "innerType": inner_spec})

    def with_attributes(self, new_attributes):
        """Creates a new spec with the same properties, updating attributes.

        :param new_attributes: The specs of the new attributes.
        :type new_attributes: list[:class:`~tamr_unify_client.attribute.resource.AttributeSpec`]
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        """
        attr_specs = [attr.to_dict() for attr in new_attributes]
        return AttributeTypeSpec({**self._data, "attributes": attr_specs})

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data!r})"
        )
