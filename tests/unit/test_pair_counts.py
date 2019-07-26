from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.mastering.estimated_pair_counts import EstimatedPairCounts
from tamr_unify_client.mastering.project import MasteringProject
from tamr_unify_client.operation import Operation


class TestPairCounts(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_get(self):
        p = MasteringProject(self.unify, self._project_json)
        responses.add(
            responses.GET,
            f"{self._url_base}/{self._api_path}",
            json=self._estimate_json,
        )
        generated = p.estimate_pairs()

        created = EstimatedPairCounts.from_json(
            self.unify, self._estimate_json, self._api_path
        )
        self.assertEqual(repr(generated), repr(created))

    def test_properties(self):
        estimate = EstimatedPairCounts.from_json(
            self.unify, self._estimate_json, self._api_path
        )
        self.assertFalse(estimate.is_up_to_date)
        self.assertEqual(estimate.total_estimate, self._estimate_json["totalEstimate"])
        self.assertEqual(
            estimate.clause_estimates, self._estimate_json["clauseEstimates"]
        )

    @responses.activate
    def test_refresh(self):
        responses.add(
            responses.POST,
            f"{self._url_base}/{self._api_path}:refresh",
            json=self._refresh_json,
        )
        updated = self._refresh_json.copy()
        updated["status"]["state"] = "SUCCEEDED"
        responses.add(responses.GET, f"{self._url_base}/operations/24", json=updated)

        estimate = EstimatedPairCounts.from_json(
            self.unify, self._estimate_json, self._api_path
        )
        generated = estimate.refresh(poll_interval_seconds=0)

        created = Operation.from_json(self.unify, updated)
        self.assertEqual(repr(generated), repr(created))

    _url_base = "http://localhost:9100/api/versioned/v1"
    _api_path = "projects/1/estimatedPairCounts"

    _project_json = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "mastering",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "mastering_unified_dataset",
        "created": {
            "username": "admin",
            "time": "2019-07-08T20:14:46.904Z",
            "version": "20",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-08T20:18:13.629Z",
            "version": "89",
        },
        "relativeId": "projects/1",
        "externalId": "1c2a10e5-e602-47ac-ade8-f9c23e49dfd2",
    }

    _estimate_json = {
        "isUpToDate": False,
        "totalEstimate": {"candidatePairCount": "150", "generatedPairCount": "75"},
        "clauseEstimates": {
            "clause1": {"candidatePairCount": "50", "generatedPairCount": "25"},
            "clause2": {"candidatePairCount": "100", "generatedPairCount": "50"},
        },
    }

    _refresh_json = {
        "id": "24",
        "type": "SPARK",
        "description": "Generate Pair Estimates",
        "status": {
            "state": "PENDING",
            "startTime": "",
            "endTime": "",
            "message": "Job has not yet been submitted to Spark",
        },
        "created": {
            "username": "admin",
            "time": "2019-07-18T15:40:26.974Z",
            "version": "1052",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-18T15:40:26.974Z",
            "version": "1052",
        },
        "relativeId": "operations/24",
    }
