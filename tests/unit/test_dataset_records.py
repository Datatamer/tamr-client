from functools import partial
from unittest import TestCase

from pandas import DataFrame
from requests.exceptions import HTTPError
import responses
import simplejson

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestDatasetRecords(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_get(self):
        records_url = f"{self._dataset_url}/records"
        responses.add(responses.GET, self._dataset_url, json={})
        responses.add(
            responses.GET,
            records_url,
            body="\n".join([simplejson.dumps(l) for l in self._records_json]),
        )

        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)
        records = list(dataset.records())
        self.assertListEqual(records, self._records_json)

    @responses.activate
    def test_update(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset._update_records(updates)
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates, False))

    @responses.activate
    def test_nan_update(self):
        def create_callback(request, snoop, status):
            snoop["payload"] = list(request.body)
            return status, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._nan_records_json)
        snoop = {}

        responses.add_callback(
            responses.POST,
            records_url,
            partial(create_callback, snoop=snoop, status=400),
        )
        responses.add_callback(
            responses.POST,
            records_url,
            partial(create_callback, snoop=snoop, status=200),
        )

        self.assertRaises(HTTPError, lambda: dataset._update_records(updates))
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates, False))

        response = dataset._update_records(updates, ignore_nan=True)
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates, True))

    @responses.activate
    def test_upsert(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.upsert_records(self._records_json, "attribute1")
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates, False))

    @responses.activate
    def test_upsert_from_dataframe(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.upsert_from_dataframe(
            self._dataframe, primary_key_name="attribute1"
        )
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates, False))

    @responses.activate
    def test_delete(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        deletes = TestDatasetRecords.records_to_deletes(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.delete_records(self._records_json, "attribute1")
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(deletes, False))

    @responses.activate
    def test_delete_ids(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, simplejson.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        deletes = TestDatasetRecords.records_to_deletes(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        ids = [r["attribute1"] for r in self._records_json]
        response = dataset.delete_records_by_id(ids)
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(deletes, False))

    @responses.activate
    def test_delete_all(self):
        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        responses.add(responses.DELETE, self._dataset_url + "/records", status=204)
        response = dataset.delete_all_records()
        self.assertEqual(response.status_code, 204)

    @staticmethod
    def records_to_deletes(records):
        return [
            {"action": "DELETE", "recordId": i}
            for i, record in enumerate(records, start=1)
        ]

    @staticmethod
    def records_to_updates(records):
        return [
            {"action": "CREATE", "recordId": i, "record": record}
            for i, record in enumerate(records, start=1)
        ]

    @staticmethod
    def stringify(updates, ignore_nan):
        return [
            simplejson.dumps(u, ignore_nan=ignore_nan).encode("utf-8") for u in updates
        ]

    _dataset_id = "1"
    _dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/{_dataset_id}"

    _records_json = [{"attribute1": 1}, {"attribute1": 2}]
    _dataframe = DataFrame(_records_json, columns=["attribute1"])
    _nan_records_json = [{"attribute1": float("nan")}, {"attribute1": float("nan")}]
    _response_json = {
        "numCommandsProcessed": 2,
        "allCommandsSucceeded": True,
        "validationErrors": [],
    }
