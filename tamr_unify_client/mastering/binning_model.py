import json

from tamr_unify_client.base_resource import BaseResource


class BinningModel(BaseResource):
    """ A binning model object."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    def records(self):
        """Stream this object's records as Python dictionaries.

        :return: Stream of records.
        :rtype: Python generator yielding :py:class:`dict`
        """
        with self.client.get(self.api_path + "/records", stream=True) as response:
            for line in response.iter_lines():
                yield json.loads(line)

    def update_records(self, records):
        """Send a batch of record creations/updates/deletions to this dataset.

        :param records: Each record should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.
        :type records: iterable[dict]
        :returns: JSON response body from server.
        :rtype: :py:class:`dict`
        """

        def _stringify_updates(updates):
            for update in updates:
                yield json.dumps(update).encode("utf-8")

        return (
            self.client.post(
                self.api_path + "/records",
                headers={"Content-Encoding": "utf-8"},
                data=_stringify_updates(records),
            )
            .successful()
            .json()
        )

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"api_path={self.api_path})"
        )
