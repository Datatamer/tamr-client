from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestCategorization(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_taxonomy(self):
        project_url = f"http://localhost:9100/api/versioned/v1/projects/1"
        taxonomy_url = f"http://localhost:9100/api/versioned/v1/projects/1/taxonomy"
        responses.add(responses.GET, project_url, json=self._project_json)
        responses.add(responses.POST, taxonomy_url, json=self._taxonomy_json)

        project = self.unify.projects.by_resource_id("1").as_categorization()
        creation_spec = {"name": "Test Taxonomy"}
        u = project.create_taxonomy(creation_spec)

        responses.add(responses.GET, taxonomy_url, json=self._taxonomy_json)
        t = project.taxonomy()
        self.assertEqual(print(u), print(t))

    _project_json = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "Test Project",
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

    _taxonomy_json = {
        "id": "unify://unified-data/v1/projects/1/taxonomy",
        "name": "Test Taxonomy",
        "created": {
            "username": "admin",
            "time": "2019-07-12T13:09:14.981Z",
            "version": "405",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-12T13:09:14.981Z",
            "version": "405",
        },
        "relativeId": "projects/1/taxonomy",
    }
