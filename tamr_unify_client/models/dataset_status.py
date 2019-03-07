from tamr_unify_client.models.base_resource import BaseResource


class DatasetStatus(BaseResource):
    """Streamability status of a Unify dataset."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "DatasetStatus":
        return super().from_data(client, resource_json, api_path)

    @property
    def dataset_name(self) -> str:
        """The name of the associated dataset.

        :type: str
        """
        return self._data["datasetName"]

    @property
    def relative_dataset_id(self) -> str:
        """The relative dataset ID of the associated dataset.

        :type: str
        """
        return self._data["relativeDatasetId"]

    @property
    def is_streamable(self) -> bool:
        """Whether the associated dataset is available to be streamed.

        :type: bool
        """
        return self._data["isStreamable"]
