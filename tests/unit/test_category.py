from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.category.resource import Category


class TestCategory(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        alias = "projects/1/taxonomy/categories/1"
        row_num = Category(self.unify, self._categories_json[0], alias)

        expected = alias
        self.assertEqual(expected, row_num.relative_id)

        expected = self._categories_json[0]["name"]
        self.assertEqual(expected, row_num.name)

        expected = self._categories_json[0]["description"]
        self.assertEqual(expected, row_num.description)

    def test_resource_from_json(self):
        alias = "projects/1/taxonomy/categories/1"
        expected = Category(self.unify, self._categories_json[0], alias)
        actual = Category.from_json(self.unify, self._categories_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    @responses.activate
    def test_path(self):
        t2 = Category(
            self.unify, self._categories_json[1], "projects/1/taxonomy/categories/2"
        )

        parent_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories/1"
        )
        responses.add(responses.GET, parent_url, json=self._categories_json[0])
        t1 = t2.parent()

        self.assertEqual(self._categories_json[0]["relativeId"], t1.relative_id)
        self.assertIsNone(t1.parent())

        self.assertEqual(t1.path, [t1.name])
        self.assertEqual(t2.path, [t1.name, t2.name])

    _categories_json = [
        {
            "id": "unify://unified-data/v1/projects/1/taxonomy/categories/1",
            "name": "t1",
            "description": "",
            "parent": "",
            "path": ["t1"],
            "created": {
                "username": "admin",
                "time": "2019-07-12T13:10:52.988Z",
                "version": "414",
            },
            "lastModified": {
                "username": "admin",
                "time": "2019-07-12T13:10:52.988Z",
                "version": "414",
            },
            "relativeId": "projects/1/taxonomy/categories/1",
        },
        {
            "id": "unify://unified-data/v1/projects/1/taxonomy/categories/2",
            "name": "t2",
            "description": "",
            "parent": "unify://unified-data/v1/projects/1/taxonomy/categories/1",
            "path": ["t1", "t2"],
            "created": {
                "username": "admin",
                "time": "2019-07-12T13:51:20.600Z",
                "version": "419",
            },
            "lastModified": {
                "username": "admin",
                "time": "2019-07-12T13:51:20.600Z",
                "version": "419",
            },
            "relativeId": "projects/1/taxonomy/categories/2",
        },
    ]
