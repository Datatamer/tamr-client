from tamr_unify_client.mastering.published_cluster.version import (
    PublishedClusterVersion,
)


class PublishedCluster:
    """A representation of a published cluster in a mastering project with version information.
    See https://docs.tamr.com/reference#retrieve-published-clusters-given-cluster-ids.

    This is not a `BaseResource` because it does not have its own API endpoint.

    :param data: The JSON entity representing this :class:`~tamr_unify_client.mastering.published_cluster.resource.PublishedCluster`.
    """

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        """:type: str"""
        return self._data.get("id")

    @property
    def versions(self):
        """:type: list[:class:`~tamr_unify_client.mastering.published_cluster.version.PublishedClusterVersion`]"""
        return [PublishedClusterVersion(v) for v in self._data.get("versions")]

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"id={self.id!r})"
        )
