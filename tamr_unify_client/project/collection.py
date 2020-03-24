from tamr_unify_client.base_collection import BaseCollection
from tamr_unify_client.project.resource import Project


class ProjectCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.project.resource.Project` s.

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
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        """
        return super().by_resource_id("projects", resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve a project by relative ID.

        :param relative_id: The resource ID. E.g. ``"projects/1"``
        :type relative_id: str
        :returns: The specified project.
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        """
        return super().by_relative_id(Project, relative_id)

    def by_external_id(self, external_id):
        """Retrieve a project by external ID.

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified project, if found.
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        :raises KeyError: If no project with the specified external_id is found
        :raises LookupError: If multiple projects with the specified external_id are found
        """
        return super().by_external_id(Project, external_id)

    def stream(self):
        """Stream projects in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of projects.
        :rtype: Python generator yielding :class:`~tamr_unify_client.project.resource.Project`

        Usage:
            >>> for project in collection.stream(): # explicit
            >>>     do_stuff(project)
            >>> for project in collection: # implicit
            >>>     do_stuff(project)
        """
        return super().stream(Project)

    def by_name(self, project_name: str) -> Project:
        """Get project by name

        Fetches a specific project in this collection by exact-match on name.

        Args:
            project_name: Name of the desired project.
        Raises:
            KeyError: If no project with specified name was found.
        """
        for project in self:
            if project.name == project_name:
                return project
        raise KeyError(f"No project found with name: {project_name}")

    def create(self, creation_spec):
        """
        Create a Project in Tamr

        :param creation_spec: Project creation specification should be formatted as specified in the `Public Docs for Creating a Project <https://docs.tamr.com/reference#create-a-project>`_.
        :type creation_spec: dict[str, str]
        :returns: The created Project
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        return Project.from_json(self.client, data)

    # super.__repr__ is sufficient
