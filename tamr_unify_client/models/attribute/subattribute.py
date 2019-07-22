class SubAttribute:
    """
    An attribute which is itself a property of another attribute.
    See https://docs.tamr.com/reference#attribute-types

    :param client: Delegate underlying API calls to this client.
    :type: :class:`~tamr_unify_client.Client`
    :param data: JSON data representing this attribute
    :type: :py:class:`dict`
    """

    def __init__(self, client, data):
        self.client = client
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
        """:type: :class:`~tamr_unify_client.models.attribute.type.AttributeType`"""
        # import locally to avoid circular dependency
        from tamr_unify_client.models.attribute.type import AttributeType

        type_json = self._data.get("type")
        return AttributeType(self.client, type_json)

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
