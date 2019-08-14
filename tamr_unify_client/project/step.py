class ProjectStep:
    """A step of a Tamr project. This is not a `BaseResource` because it has no API path
    and cannot be directly retrieved or modified.

    See https://docs.tamr.com/reference#retrieve-downstream-dataset-usage

    :param client: Delegate underlying API calls to this client.
    :type client: :class:`~tamr_unify_client.Client`
    :param data: The JSON body containing project step information.
    :type data: :py:class:`dict`
    """

    def __init__(self, client, data):
        self.client = client
        self._data = data

    @property
    def project_step_id(self):
        """:type: str"""
        return self._data.get("projectStepId")

    @property
    def project_step_name(self):
        """:type: str"""
        return self._data.get("projectStepName")

    @property
    def project_name(self):
        """:type: str"""
        return self._data.get("projectName")

    @property
    def type(self):
        """A Tamr project type, listed in https://docs.tamr.com/reference#create-a-project.

        :type: str"""
        return self._data.get("type")

    def project(self):
        """Retrieves the :class:`~tamr_unify_client.project.resource.Project` this step is associated with.

        :returns: This step's project.
        :rtype: :class:`~tamr_unify_client.project.resource.Project`
        :raises KeyError: If no project with the specified name is found.
        :raises LookupError: If multiple projects with the specified name are found.
        """
        name = self.project_name
        projects = [p for p in self.client.projects if p.name == name]

        if len(projects) == 0:
            raise KeyError(f'No project found with name "{name}"')
        elif len(projects) > 1:
            raise LookupError(f'Multiple projects found with name "{name}"')

        return projects[0]

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"project_step_id={self.project_step_id!r}, "
            f"project_step_name={self.project_step_name!r}, "
            f"project_name={self.project_name!r}, "
            f"type={self.type!r})"
        )
