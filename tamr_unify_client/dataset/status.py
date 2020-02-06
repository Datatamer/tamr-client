from tamr_unify_client.base_resource import BaseResource


class DatasetStatus(BaseResource):
    """Streamability status of a Tamr dataset."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "DatasetStatus":
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
    def is_streamable(self) -> bool:
        """Whether the associated dataset is available to be streamed.

        :type: bool
        """
        return self._data.get("isStreamable")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"dataset_name={self.dataset_name!r}, "
            f"relative_dataset_id={self.relative_dataset_id!r}, "
            f"is_streamable={self.is_streamable!r})"
        )
