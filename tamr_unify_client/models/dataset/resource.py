import json

from tamr_unify_client.models.base_resource import BaseResource
from tamr_unify_client.models.operation import Operation


class Dataset(BaseResource):
    """A Unify dataset."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    @property
    def name(self):
        """:type: str"""
        return self.data["name"]

    @property
    def description(self):
        """:type: str"""
        return self.data["description"]

    @property
    def version(self):
        """:type: str"""
        return self.data["version"]

    @property
    def tags(self):
        """:type: list[str]"""
        return self.data["tags"]

    def update_records(self, records):
        """Send a batch of record creations/updates/deletions to this dataset.

        :param records: Each record should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.
        :type records: list[dict]
        """
        body = "\n".join([json.dumps(r) for r in records])
        self.client.post(self.api_path + ":updateRecords", data=body)

    def refresh(self, **options):
        """Brings dataset up-to-date if needed, taking whatever actions are required.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        """
        op_json = self.client.post(self.api_path + ":refresh").successful().json()
        op = Operation.from_json(self.client, op_json)
        return op.apply_options(**options)

    def records(self):
        """Stream this dataset's records as Python dictionaries.

        :return: Stream of records.
        :rtype: Python generator yielding :py:class:`dict`
        """
        with self.client.get(self.api_path + "/records", stream=True) as response:
            for line in response.iter_lines():
                yield json.loads(line)
