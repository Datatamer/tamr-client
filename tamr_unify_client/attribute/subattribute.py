class SubAttribute:
    """
    An attribute which is itself a property of another attribute.

    See https://docs.tamr.com/reference#attribute-types

    :param data: JSON data representing this attribute
    :type data: :py:class:`dict`
    """

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def type(self):
        """:type: :class:`~tamr_unify_client.attribute.type.AttributeType`"""
        # import locally to avoid circular dependency
        from tamr_unify_client.attribute.type import AttributeType

        type_json = self._data.get("type")
        return AttributeType(type_json)

    @property
    def is_nullable(self):
        """:type: bool"""
        return self._data.get("isNullable")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"name={self.name!r})"
        )
