class RecordPublishedClusterVersion:
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
    def cluster_id(self):
        """:type: str"""
        return self._data.get("clusterId")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"version={self.version!r}, "
            f"timestamp={self.timestamp!r}, "
            f"name={self.cluster_id!r})"
        )
