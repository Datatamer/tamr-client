from tamr_unify_client.mastering.published_cluster.record_version import (
    RecordPublishedClusterVersion,
)


class RecordPublishedCluster:
    """A representation of a published cluster of a record in a mastering project with version information.
    See https://docs.tamr.com/reference#retrieve-published-clusters-given-record-ids.

    This is not a `BaseResource` because it does not have its own API endpoint.

    :param data: The JSON entity representing this
        :class:`~tamr_unify_client.mastering.published_cluster.record.RecordPublishedCluster`.
    """

    def __init__(self, data):
        self._data = data

    @property
    def entity_id(self):
        """:type: str"""
        return self._data.get("entityId")

    @property
    def source_id(self):
        """:type: str"""
        return self._data.get("sourceId")

    @property
    def origin_entity_id(self):
        """:type: str"""
        return self._data.get("originEntityId")

    @property
    def origin_source_id(self):
        """:type: str"""
        return self._data.get("originSourceId")

    @property
    def versions(self):
        """:type: list[:class:`~tamr_unify_client.mastering.published_cluster.record_version.RecordPublishedClusterVersion`]"""
        return [RecordPublishedClusterVersion(v) for v in self._data.get("versions")]

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"entity_id={self.entity_id!r}, "
            f"source_id={self.source_id!r}, "
            f"origin_entity_id={self.origin_entity_id!r}, "
            f"origin_source_id={self.origin_source_id!r})"
        )
