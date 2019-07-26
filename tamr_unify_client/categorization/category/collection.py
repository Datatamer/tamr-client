import json

from tamr_unify_client.base_collection import BaseCollection
from tamr_unify_client.categorization.category.resource import Category


class CategoryCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.categorization.category.resource.Category` s.

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
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.Category`
        """
        return super().by_resource_id(self.api_path, resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve a category by relative ID.

        :param relative_id: The relative ID. E.g. ``"projects/1/categories/1"``
        :type relative_id: str
        :returns: The specified category.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.Category`
        """
        return super().by_relative_id(Category, relative_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute by external ID.

        Since categories do not have external IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified category, if found.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.Category`
        :raises KeyError: If no category with the specified external_id is found
        :raises LookupError: If multiple categories with the specified external_id are found
        """
        raise NotImplementedError("Categories do not have external_id")

    def stream(self):
        """Stream categories in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of categories.
        :rtype: Python generator yielding :class:`~tamr_unify_client.categorization.category.resource.Category`

        Usage:
            >>> for category in collection.stream(): # explicit
            >>>     do_stuff(category)
            >>> for category in collection: # implicit
            >>>     do_stuff(category)
        """
        return super().stream(Category)

    def create(self, creation_spec):
        """ Creates a new category.

        :param creation_spec: Category creation specification, formatted as specified in the
            `Public Docs for Creating a Category <https://docs.tamr.com/reference#create-a-category>`_.
        :type creation_spec: dict
        :return: The newly created category.
        :rtype: :class:`~tamr_unify_client.categorization.category.resource.Category`
        """
        resource_json = (
            self.client.post(self.api_path, json=creation_spec).successful().json()
        )
        return Category.from_json(self.client, resource_json)

    def bulk_create(self, creation_specs):
        """Creates new categories in bulk.

        :param creation_specs: A collection of creation specifications, as detailed for create.
        :type creation_specs: iterable[dict]
        :returns: JSON response from the server
        :rtype: :py:class:`dict`
        """
        body = "\n".join([json.dumps(s) for s in creation_specs]).encode("utf-8")
        return (
            self.client.post(
                self.api_path + ":bulk",
                headers={"Content-Encoding": "utf-8"},
                data=body,
            )
            .successful()
            .json()
        )

    # super.__repr__ is sufficient
