from tamr_unify_client.models.base_resource import BaseResource
from tamr_unify_client.models.operation import Operation


class MachineLearningModel(BaseResource):
    """A Unify Machine Learning model."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    def train(self, **options):
        """Learn from verified labels.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        """
        op_json = self.client.post(self.api_path + ":refresh").successful().json()
        op = Operation.from_json(self.client, op_json)
        return op.apply_options(**options)

    def predict(self, **options):
        """Suggest labels for unverified records.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        """
        dependent_dataset = "/".join(self.api_path.split("/")[:-1])
        op_json = self.client.post(dependent_dataset + ":refresh").successful().json()
        op = Operation.from_json(self.client, op_json)
        return op.apply_options(**options)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r})"
        )
