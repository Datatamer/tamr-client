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

        :return: A dictionary containing candidate pairs and estimated pairs mapped to their corresponding estimated counts
                For example: 
                {
                    "candidatePairCount": "54321",
                    "generatedPairCount": "12345"
                }
        :rtype: dict[str, int]
        """
        return self._data.get("totalEstimate")

    @property
    def clause_estimates(self) -> dict:
        """The estimated candidate pair count and generated pair count for each clause in the model.

        :return: A dictionary containing each clause name mapped to a dictionary containing the corresponding estimated candidate and generated pair counts
                For example:
                  {
                    "Clause1": {
                      "candidatePairCount": "321",
                      "generatedPairCount": "123"
                    },
                    "Clause2": {
                      "candidatePairCount": "654",
                      "generatedPairCount": "456"
                    }
                  }
        :rtype: dict[str, dict[str, int]]
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
