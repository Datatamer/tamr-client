from tamr_unify_client.base_resource import BaseResource
from tamr_unify_client.operation import Operation


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

        :return: A dictionary containing candidate pairs and estimated pairs mapped to their corresponding estimated counts.
            For example:\n
            {\n
                "candidatePairCount": "54321",\n
                "generatedPairCount": "12345"\n
            }
        :rtype: dict[str, str]
        """
        return self._data.get("totalEstimate")

    @property
    def clause_estimates(self) -> dict:
        """The estimated candidate pair count and generated pair count for each clause in the model.

        :return: A dictionary containing each clause name mapped to a dictionary containing the corresponding estimated candidate and generated pair counts.
            For example:\n
            {\n
                "Clause1": {\n
                    "candidatePairCount": "321",\n
                    "generatedPairCount": "123"\n
                },\n
                "Clause2": {\n
                    "candidatePairCount": "654",\n
                    "generatedPairCount": "456"\n
                }\n
            }
        :rtype: dict[str, dict[str, str]]
        """
        return self._data.get("clauseEstimates")

    def refresh(self, **options):
        """Updates the estimated pair counts if needed.

        The pair count estimates are updated on the server; you will need to call
        :func:`~tamr_unify_client.mastering.project.MasteringProject.estimate_pairs`
        to retrieve the updated estimate.

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
            f"up_to_date={self.is_up_to_date!r}, "
            f"total_estimate={self.total_estimate!r}, "
            f"clause_estimates={self.clause_estimates!r})"
        )
