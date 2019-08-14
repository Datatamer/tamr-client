class DatasetURI:
    """
    Indentifier of a dataset.

    :param client: Queried dataset's client.
    :type client: :class:`~tamr_unify_client.client.Client`
    :param uri: Queried dataset's dataset ID.
    :type uri: :py:class:`str`
    """

    def __init__(self, client, uri):
        self.client = client
        self._uri = uri

    @property
    def resource_id(self):
        """:type: str"""
        return self._uri.split("/")[-1]

    @property
    def relative_id(self):
        """:type: str"""
        return "datasets/" + self.resource_id

    @property
    def uri(self):
        """:type: str"""
        return self._uri

    def dataset(self):
        """Fetch the dataset that this identifier points to.

        :return: A Tamr dataset.
        :rtype: :class: `~tamr_unify_client.dataset.resource.Dataset`
        """
        return self.client.datasets.by_resource_id(self.resource_id)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"'{self.uri})'"
        )
