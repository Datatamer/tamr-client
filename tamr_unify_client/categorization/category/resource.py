from copy import deepcopy

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
        return self._data.get("path")[:]

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

    def spec(self):
        """Returns this category's spec.

        :return: The spec for the category.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return CategorySpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r},"
            f"path={'/'.join(self.path)!r},"
            f"description={self.description!r})"
        )


class CategorySpec:
    """A representation of the server view of a category."""

    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates a category spec from a category.

        :param resource: The existing category.
        :type resource: :class:`~tamr_unify_client.categorization.category.resource.Category`
        :return: The corresponding category spec.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return CategorySpec(
            resource.client, deepcopy(resource._data), resource.api_path
        )

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new category.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return CategorySpec(None, {}, None)

    def from_data(self, data):
        """Creates a spec with the same client and API path as this one, but new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return CategorySpec(self.client, data, self.api_path)

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
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return self.from_data({**self._data, "name": new_name})

    def with_description(self, new_description):
        """Creates a new spec with the same properties, updating description.

        :param new_description: The new description.
        :type new_description: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return self.from_data({**self._data, "description": new_description})

    def with_path(self, new_path):
        """Creates a new spec with the same properties, updating path.

        :param new_path: The new path.
        :type new_path: list[str]
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.CategorySpec`
        """
        return self.from_data({**self._data, "path": new_path})

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )
