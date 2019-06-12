from tamr_unify_client.models.base_resource import BaseResource


class EstimatedPairCounts(BaseResource):
    """Estimated Pair Counts info for Mastering Project"""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "EstimatedPairCounts":
        return super().from_data(client, resource_json, api_path)

    @property
    def is_up_to_date(self) -> bool:
        """Whether an estimate pairs job has been run since the last edit to the binning model.

        :rtype: bool
        """
        return self._data.get("isUpToDate")

    @property
    def total_estimate(self) -> dict:
        """The total number of estimated candidate pairs and generated pairs for the model across all clauses.

        :return: Candidate pairs and estimated pairs with corresponding estimated counts
        :rtype: dict[str, int]
        """
        return self._data.get("totalEstimate")

    @property
    def clause_estimates(self) -> dict:
        """The estimated candidate pair count and generated pair count for each clause in the model.

        :return: Each clause with corresponding estimated candidate pair count and generated pair count.
        :rtype: dict[str, [dict[str, int]]
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
