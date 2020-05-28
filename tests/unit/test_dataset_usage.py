from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.dataset.resource import Dataset
from tamr_unify_client.dataset.usage import DatasetUsage
from tamr_unify_client.dataset.use import DatasetUse
from tamr_unify_client.project.step import ProjectStep


class TestUsage(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_get_usage(self):
        responses.add(
            responses.GET, f"{self._base_url}/datasets/1/usage", json=self._usage_json
        )
        u = Dataset(self.tamr, self._dataset_json).usage()
        self.assertEqual(u._data, self._usage_json)

    def test_usage(self):
        alias = "datasets/1/usage"
        u = DatasetUsage(self.tamr, self._usage_json, alias)
        self.assertEqual(u.usage._data, self._usage_json["usage"])
        self.assertEqual(u.relative_id, alias)

        udeps = u.dependencies
        deps = [DatasetUse(self.tamr, dep) for dep in self._usage_json["dependencies"]]
        for i in range(len(deps)):
            self.assertEqual(deps[i].dataset_id, udeps[i].dataset_id)

    @responses.activate
    def test_use(self):
        usage_json = self._usage_json["usage"]
        u = DatasetUse(self.tamr, usage_json)

        responses.add(
            responses.GET, f"{self._base_url}/datasets/1", json=self._dataset_json
        )

        self.assertEqual(u.dataset_id, usage_json["datasetId"])
        self.assertEqual(u.dataset_name, usage_json["datasetName"])

        self.assertEqual(u.output_from_project_steps, [])
        inputs = u.input_to_project_steps
        step = ProjectStep(self.tamr, usage_json["inputToProjectSteps"][0])
        self.assertEqual(len(inputs), 1)
        self.assertEqual(repr(inputs[0]), repr(step))

        dataset = u.dataset()
        self.assertEqual(dataset.relative_id, "datasets/1")

    @responses.activate
    def test_project_step(self):
        step_json = self._usage_json["usage"]["inputToProjectSteps"][0]
        step = ProjectStep(self.tamr, step_json)

        self.assertEqual(step.project_step_id, step_json["projectStepId"])
        self.assertEqual(step.project_step_name, step_json["projectStepName"])
        self.assertEqual(step.project_name, step_json["projectName"])
        self.assertEqual(step.type, step_json["type"])

        responses.add(
            responses.GET, f"{self._base_url}/projects", json=self._projects_json
        )
        project = step.project()
        self.assertEqual(project.relative_id, self._projects_json[0]["relativeId"])

    _base_url = "http://localhost:9100/api/versioned/v1"

    _dataset_json = {
        "id": "unify://unified-data/v1/datasets/1",
        "name": "myData.csv",
        "description": "",
        "version": "321",
        "keyAttributeNames": ["pk"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2019-07-08T20:15:06.818Z",
            "version": "4",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-18T17:58:38.453Z",
            "version": "6125",
        },
        "relativeId": "datasets/1",
        "upstreamDatasetIds": [],
        "externalId": "myData.csv",
    }

    _projects_json = [
        {
            "id": "unify://unified-data/v1/projects/1",
            "name": "My Project",
            "description": "Categorization Project",
            "type": "CATEGORIZATION",
            "unifiedDatasetName": "",
            "created": {
                "username": "admin",
                "time": "2019-07-12T13:08:17.440Z",
                "version": "401",
            },
            "lastModified": {
                "username": "admin",
                "time": "2019-07-12T13:08:17.534Z",
                "version": "402",
            },
            "relativeId": "projects/1",
            "externalId": "904bf89e-74ba-45c5-8b4a-5ff913728f66",
        }
    ]

    _usage_json = {
        "usage": {
            "datasetId": "unify://unified-data/v1/datasets/1",
            "datasetName": "myData.csv",
            "inputToProjectSteps": [
                {
                    "projectStepId": "unify://unified-data/v1/projectSteps/1",
                    "projectStepName": "My Project-SCHEMA_MAPPING",
                    "projectName": "My Project",
                    "type": "SCHEMA_MAPPING",
                }
            ],
            "outputFromProjectSteps": [],
        },
        "dependencies": [
            {
                "datasetId": "unify://unified-data/v1/datasets/2",
                "datasetName": "myData.csv_sample",
                "inputToProjectSteps": [],
                "outputFromProjectSteps": [],
            },
            {
                "datasetId": "unify://unified-data/v1/datasets/3",
                "datasetName": "My Project - Unified Dataset",
                "inputToProjectSteps": [
                    {
                        "projectStepId": "unify://unified-data/v1/projectSteps/2",
                        "projectStepName": "My Project-SCHEMA_MAPPING_RECOMMENDATIONS",
                        "projectName": "My Project",
                        "type": "SCHEMA_MAPPING_RECOMMENDATIONS",
                    },
                    {
                        "projectStepId": "unify://unified-data/v1/projectSteps/3",
                        "projectStepName": "My Project-CATEGORIZATION",
                        "projectName": "My Project",
                        "type": "CATEGORIZATION",
                    },
                ],
                "outputFromProjectSteps": [
                    {
                        "projectStepId": "unify://unified-data/v1/projectSteps/1",
                        "projectStepName": "My Project-SCHEMA_MAPPING",
                        "projectName": "My Project",
                        "type": "SCHEMA_MAPPING",
                    },
                    {
                        "projectStepId": "unify://unified-data/v1/projectSteps/2",
                        "projectStepName": "My Project-SCHEMA_MAPPING_RECOMMENDATIONS",
                        "projectName": "MY Project",
                        "type": "SCHEMA_MAPPING_RECOMMENDATIONS",
                    },
                ],
            },
        ],
    }
