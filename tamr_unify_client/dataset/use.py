from tamr_unify_client.project.step import ProjectStep


class DatasetUse:
    """
    The use of a dataset in project steps. This is not a `BaseResource` because it has no API path
    and cannot be directly retrieved or modified.

    See https://docs.tamr.com/reference#retrieve-downstream-dataset-usage

    :param client: Delegate underlying API calls to this client.
    :type client: :class:`~tamr_unify_client.Client`
    :param data: The JSON body containing usage information.
    :type data: :py:class:`dict`
    """

    def __init__(self, client, data):
        self.client = client
        self._data = data

    @property
    def dataset_id(self):
        """:type: str"""
        return self._data.get("datasetId")

    @property
    def dataset_name(self):
        """:type: str"""
        return self._data.get("datasetName")

    @property
    def input_to_project_steps(self):
        """:type: list[:class:`~tamr_unify_client.project.step.ProjectStep`]"""
        steps = self._data.get("inputToProjectSteps")
        return [ProjectStep(self.client, step) for step in steps]

    @property
    def output_from_project_steps(self):
        """:type: list[:class:`~tamr_unify_client.project.step.ProjectStep`]"""
        steps = self._data.get("outputFromProjectSteps")
        return [ProjectStep(self.client, step) for step in steps]

    def dataset(self):
        """Retrieves the :class:`~tamr_unify_client.dataset.resource.Dataset` this use represents.

        :return: The dataset being used.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        dataset_id = self.dataset_id.split("/")[-1]
        return self.client.datasets.by_resource_id(dataset_id)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dataset_id={self.dataset_id!r})"
        )
