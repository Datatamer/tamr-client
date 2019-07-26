from tamr_unify_client.base_resource import BaseResource


class Category(BaseResource):
    """A category of a taxonomy"""

    @classmethod
    def from_json(cls, client, data, api_path=None):
        return super().from_data(client, data, api_path)

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def path(self):
        """:type: list[str]"""
        return self._data.get("path")

    def parent(self):
        """Gets the parent Category of this one, or None if it is a tier 1 category

        :returns: The parent Category or None
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.Category`
        """
        parent = self._data.get("parent")
        if parent:
            alias = self.api_path.rsplit("/", 1)[0] + "/" + parent.split("/")[-1]
            resource_json = self.client.get(alias).successful().json()
            return Category.from_json(self.client, resource_json, alias)
        else:
            return None

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r},"
            f"path={'/'.join(self.path)!r},"
            f"description={self.description!r})"
        )
