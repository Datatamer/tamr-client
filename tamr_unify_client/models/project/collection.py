from tamr_unify_client.models.base_collection import BaseCollection
from tamr_unify_client.models.project.resource import Project


class ProjectCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.models.project.resource.Project` s.

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path used to access this collection.
        Default: ``"projects"``.
    :type api_path: str
    """

    def __init__(self, client, api_path="projects"):
        super().__init__(client, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve a project by resource ID.

        :param resource_id: The resource ID. E.g. ``"1"``
        :type resource_id: str
        :returns: The specified project.
        :rtype: :class:`~tamr_unify_client.models.project.resource.Project`
        """
        return super().by_resource_id("projects", resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve a project by relative ID.

        :param relative_id: The resource ID. E.g. ``"projects/1"``
        :type relative_id: str
        :returns: The specified project.
        :rtype: :class:`~tamr_unify_client.models.project.resource.Project`
        """
        return super().by_relative_id(Project, relative_id)

    def stream(self):
        """Stream projects in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of projects.
        :rtype: Python generator yielding :class:`~tamr_unify_client.models.project.resource.Project`

        Usage:
            >>> for project in collection.stream(): # explicit
            >>>     do_stuff(project)
            >>> for project in collection: # implicit
            >>>     do_stuff(project)
        """
        return super().stream(Project)
