class Metric:
    """ A metric for a published cluster.

    This is not a `BaseResource` because it does not have its own API endpoint.

    :param data: The JSON entity representing this cluster.
    """

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        """:type: str"""
        return self._data.get("metricName")

    @property
    def value(self):
        """:type: str"""
        return self._data.get("metricValue")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"name={self.name!r}, "
            f"value={self.value!r})"
        )
