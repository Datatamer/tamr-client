from tamr_unify_client.mastering.published_cluster.metric import Metric


class PublishedClusterVersion:
    """A version of a published cluster in a mastering project.

    This is not a `BaseResource` because it does not have its own API endpoint.

    :param data: The JSON entity representing this version.
    """

    def __init__(self, data):
        self._data = data

    @property
    def version(self):
        """:type: str"""
        return self._data.get("version")

    @property
    def timestamp(self):
        """:type: str"""
        return self._data.get("timestamp")

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    @property
    def metrics(self):
        """:type: list[:class:`~tamr_unify_client.mastering.published_cluster.metric.Metric`]"""
        return [Metric(m) for m in self._data.get("metrics")]

    @property
    def record_ids(self):
        """:type: list[dict[str, str]]"""
        return self._data.get("recordIds")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"version={self.version!r}, "
            f"timestamp={self.timestamp!r}, "
            f"name={self.name!r})"
        )
