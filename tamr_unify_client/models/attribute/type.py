from tamr_unify_client.models.base_resource import BaseResource


class AttributeType(BaseResource):
    @classmethod
    def from_json(cls, client, data, api_path):
        return super().from_data(client, data, api_path)

    @property
    def relative_id(self):
        return self.api_path

    @property
    def base_type(self):
        """:type: str"""
        return self._data.get("baseType")

    @property
    def inner_type(self):
        """:type: :class:`~tamr_unify_client.models.attribute.type.AttributeType`"""
        if "innerType" in self._data:
            alias = self.api_path + "/type"
            return AttributeType.from_data(
                self.client, self._data.get("innerType"), alias
            )
        else:
            return None

    @property
    def attributes(self):
        """:type: :class:`~tamr_unify_client.models.attribute.collection.AttributeCollection`"""
        alias = self.api_path + "/attributes"
        collection_json = self._data.get("attributes")
        # Import locally to avoid circular dependency
        from tamr_unify_client.models.attribute.collection import AttributeCollection

        return AttributeCollection.from_json(self.client, collection_json, alias)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"base_type={self.base_type!r})"
        )
