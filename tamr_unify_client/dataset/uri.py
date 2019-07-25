class DatasetURI:
    """An upstream dataset."""

    def __init__(self, client, _uri):
        self.client = client
        self._uri = _uri

    @property
    def resource_id(self):
        """:type: str"""
        return self.dataset_id.split("/")[-1]

    @property
    def relative_id(self):
        """:type: str"""
        return "datasets/" + self.resource_id

    @property
    def uri(self):
        """:type: str"""
        return self._uri

    def __repr__(self):

        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"{self.uri}"
        )
