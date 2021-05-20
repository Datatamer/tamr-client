from tamr_unify_client.base_resource import BaseResource
from tamr_unify_client.dataset.use import DatasetUse


class DatasetUsage(BaseResource):
    """
    The usage of a dataset and its downstream dependencies.

    See https://docs.tamr.com/reference#retrieve-downstream-dataset-usage
    """

    @classmethod
    def from_json(cls, client, resource_json, api_path):
        return super().from_data(client, resource_json, api_path)

    @property
    def relative_id(self):
        """:type: str"""
        return self.api_path

    @property
    def usage(self):
        """:type: :class:`~tamr_unify_client.dataset.use.DatasetUse`"""
        return DatasetUse(self.client, self._data.get("usage"))

    @property
    def dependencies(self):
        """:type: list[:class:`~tamr_unify_client.dataset.use.DatasetUse`]"""
        deps = self._data.get("dependencies")
        return [DatasetUse(self.client, dep) for dep in deps]

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"alias={self.api_path!r})"
        )
