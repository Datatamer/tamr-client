from abc import abstractmethod
from collections.abc import Iterable


class BaseCollection(Iterable):
    """Base class for client-side collections.

    :param client: Delegate underlying API calls to this client.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path for this collection. E.g. ``"projects/1/inputDatasets"``.
    :type api_path: str
    """

    def __init__(self, client, api_path):
        self.client = client
        self.api_path = api_path

    @abstractmethod
    def by_resource_id(self, canonical_path, resource_id):
        """Retrieve an item in this collection by resource ID.

        Subclasses should override this method and pass in the specific
        ``canonical_path`` for that collection.

        :param canonical_path: The canonical (i.e. unaliased) API path for this collection.
        :type canonical_path: str
        :param resource_id: The resource ID. E.g. "1"
        :type resource_id: str
        :returns: The specified item.
        :rtype: The ``resource_class``  for this collection. See :func:`~tamr_unify_client.models.base_collection.BaseCollection.by_relative_id`.
        """
        relative_id = canonical_path + "/" + resource_id
        return self.by_relative_id(relative_id)

    @abstractmethod
    def by_relative_id(self, resource_class, relative_id):
        """Retrieve an item in this collection by relative ID.

        Subclasses should override this method and pass in the specific
        ``resource_class`` for that collection.

        :param resource_class: Resource class corresponding to items in this collection.
        :type resource_class: Python class
        :param relative_id: The relative ID. E.g. "projects/1"
        :type relative_id: str
        :returns: The specified item.
        :rtype: ``resource_class``
        """
        resource_json = self.client.get(relative_id).successful().json()
        return resource_class.from_json(
            self.client, resource_json, api_path=relative_id
        )

    @abstractmethod
    def stream(self, resource_class):
        """Stream items in this collection.

        Subclasses should override this method and pass in the specific
        ``resource_class`` for that collection.

        :param resource_class: Resource class corresponding to items in this collection.
        :type resource_class: Python class
        :returns: Generator that yields each item.
        :rtype: Python generator of ``resource_class``
        """
        resources = self.client.get(self.api_path).successful().json()
        for resource_json in resources:
            yield resource_class.from_json(self.client, resource_json)

    def __iter__(self):
        return self.stream()
