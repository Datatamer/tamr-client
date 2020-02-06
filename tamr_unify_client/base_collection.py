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
        :rtype: The ``resource_class``  for this collection. See :func:`~tamr_unify_client.base_collection.BaseCollection.by_relative_id`.
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

    @abstractmethod
    def by_external_id(self, resource_class, external_id):
        """Retrieve an item in this collection by external ID.

        Subclasses should override this method and pass in the specific
        ``resource_class`` for that collection.

        :param resource_class: Resource class corresponding to items in this collection.
        :type resource_class: Python class
        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified item, if found.
        :rtype: ``resource_class``
        :raises KeyError: If no resource with the specified external_id is found
        :raises LookupError: If multiple resources with the specified external_id are found
        """
        params = {"filter": "externalId==" + external_id}
        resources = self.client.get(self.api_path, params=params).successful().json()
        items = [
            resource_class.from_json(self.client, resource_json)
            for resource_json in resources
        ]

        if len(items) == 0:
            raise KeyError(f'No item found with external ID "{external_id}"')
        elif len(items) > 1:
            raise LookupError(
                f'More than one item found with external ID "{external_id}"'
            )

        return items[0]

    def delete_by_resource_id(self, resource_id):
        """Deletes a resource from this collection by resource ID.

        :param resource_id: The resource ID of the resource that will be deleted.
        :type resource_id: str
        :return: HTTP response from the server.
        :rtype: :class:`requests.Response`
        """
        path = f"{self.api_path}/{resource_id}"
        response = self.client.delete(path).successful()
        return response

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"api_path={self.api_path!r})"
        )
