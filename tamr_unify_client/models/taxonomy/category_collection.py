from tamr_unify_client.models.base_collection import BaseCollection
from tamr_unify_client.models.taxonomy.category import Category


class CategoryCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.models.dataset.resource.Category` s.

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path used to access this collection.
        E.g. ``"projects/1/taxonomy/categories"``.
    :type api_path: str
    """

    def __init__(self, client, api_path):
        super().__init__(client, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve a  category by resource ID.

        :param resource_id: The resource ID. E.g. ``"1"``
        :type resource_id: str
        :returns: The specified category.
        :rtype: :class:`~tamr_unify_client.models.taxonomy.resource.Category`
        """
        return super().by_resource_id(self.api_path, resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve a category by relative ID.

        :param relative_id: The resource ID. E.g. ``"categories/1"`` or ``"projects/1/categories/1"``
        :type relative_id: str
        :returns: The specified category.
        :rtype: :class:`~tamr_unify_client.models.taxonomy.resource.Category`
        """
        resource_id = relative_id.split("/")[-1]
        return self.by_resource_id(resource_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute by external ID.

        Since categories do not have external IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified category, if found.
        :rtype: :class:`~tamr_unify_client.models.taxonomy.category.Category`
        :raises KeyError: If no category with the specified external_id is found
        :raises LookupError: If multiple categories with the specified external_id are found
        """
        raise NotImplementedError("Categories do not have external_id")

    def stream(self):
        """Stream categories in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of categories.
        :rtype: Python generator yielding :class:`~tamr_unify_client.models.taxonomy.category.Category`

        Usage:
            >>> for category in collection.stream(): # explicit
            >>>     do_stuff(category)
            >>> for category in collection: # implicit
            >>>     do_stuff(category)
        """
        return super().stream(Category)

    def create(self, creation_spec):
        """ Creates a new category.

        :param creation_spec:
        :type: dict
        :return: The newly created category.
        :rtype: :class:`~tamr_unify_client.models.taxonomy.resource.Category`
        """
        resource_json = (
            self.client.post(self.api_path, json=creation_spec).successful().as_json()
        )
        return Category.from_json(self.client, resource_json)

    # super.__repr__ is sufficient
