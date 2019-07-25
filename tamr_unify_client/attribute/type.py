from tamr_unify_client.attribute.subattribute import SubAttribute


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
        collection_json = self._data.get("attributes")
        return [SubAttribute(attr) for attr in collection_json]

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"base_type={self.base_type!r})"
        )
