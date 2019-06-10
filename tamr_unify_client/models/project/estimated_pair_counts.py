from tamr_unify_client.models.base_resource import BaseResource


class EstimatedPairCounts(BaseResource):
    """Estimated Pair Counts info for Mastering Project"""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "EstimatedPairCounts":
        return super().from_data(client, resource_json, api_path)

    @property
    def is_up_to_date(self) -> bool:
        """Whether the associated dataset is up to date.

        :type: bool
        """
        return self._data.get("isUpToDate")

    @property
    def total_estimate(self) -> dict:
        """Info about when profile info was generated.

        :type: dict
        """
        return self._data.get("totalEstimate")

    @property
    def clause_estimates(self) -> dict:
        """Info about when profile info was generated.

        :type: dict
        """
        return self._data.get("clauseEstimates")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"up_to_date={self.is_up_to_date!r}, "
            f"total_estimate={self.total_estimate!r}, "
            f"clause_estimates={self.clause_estimates!r})"
        )
