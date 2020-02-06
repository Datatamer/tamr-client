from tamr_unify_client.base_resource import BaseResource
from tamr_unify_client.operation import Operation


class DatasetProfile(BaseResource):
    """Profile info of a Tamr dataset."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "DatasetProfile":
        return super().from_data(client, resource_json, api_path)

    @property
    def dataset_name(self) -> str:
        """The name of the associated dataset.

        :type: str
        """
        return self._data.get("datasetName")

    @property
    def relative_dataset_id(self) -> str:
        """The relative dataset ID of the associated dataset.

        :type: str
        """
        return self._data.get("relativeDatasetId")

    @property
    def is_up_to_date(self) -> bool:
        """Whether the associated dataset is up to date.

        :type: bool
        """
        return self._data.get("isUpToDate")

    @property
    def profiled_data_version(self) -> str:
        """The profiled data version.

        :type: str
        """
        return self._data.get("profiledDataVersion")

    @property
    def profiled_at(self) -> dict:
        """Info about when profile info was generated.

        :type: dict
        """
        return self._data.get("profiledAt")

    @property
    def simple_metrics(self) -> list:
        """Simple metrics for profiled dataset.

        :type: list
        """
        return self._data.get("simpleMetrics")

    @property
    def attribute_profiles(self) -> list:
        """Simple metrics for profiled dataset.

        :type: list
        """
        return self._data.get("attributeProfiles")

    def refresh(self, **options):
        """Updates the dataset profile if needed.

        The dataset profile is updated on the server; you will need to call
        :func:`~tamr_unify_client.dataset.resource.Dataset.profile`
        to retrieve the updated profile.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.operation.Operation` .
            See :func:`~tamr_unify_client.operation.Operation.apply_options` .
        :returns: The refresh operation.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        response = self.client.post(self.api_path + ":refresh").successful()
        op = Operation.from_response(self.client, response)
        return op.apply_options(**options)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"dataset_name={self.dataset_name!r}, "
            f"relative_dataset_id={self.relative_dataset_id!r}, "
            f"is_up_to_date={self.is_up_to_date!r}, "
            f"profiled_data_version={self.profiled_data_version!r}, "
            f"profiled_at={self.profiled_at!r}, "
            f"simple_metrics={self.simple_metrics!r})"
        )
