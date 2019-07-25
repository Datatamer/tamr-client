from functools import partial
import json
from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.category.collection import CategoryCollection
from tamr_unify_client.category.resource import Category
from tamr_unify_client.models.taxonomy.resource import Taxonomy


class TestTaxonomy(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_categories(self):
        cat_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories"
        )
        responses.add(responses.GET, cat_url, json=self._categories_json)

        t = Taxonomy(self.unify, self._taxonomy_json)
        c = list(t.categories())

        cats = [
            Category(self.unify, self._categories_json[0]),
            Category(self.unify, self._categories_json[1]),
        ]
        self.assertEqual(repr(c), repr(cats))

    @responses.activate
    def test_by_id(self):
        cat_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories/1"
        )
        responses.add(responses.GET, cat_url, json=self._categories_json[0])

        c = CategoryCollection(self.unify, "projects/1/taxonomy/categories")
        r = c.by_relative_id("projects/1/taxonomy/categories/1")
        self.assertEqual(r._data, self._categories_json[0])
        r = c.by_resource_id("1")
        self.assertEqual(r._data, self._categories_json[0])
        self.assertRaises(NotImplementedError, c.by_external_id, "1")

    @responses.activate
    def test_create(self):
        post_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories"
        )
        responses.add(responses.POST, post_url, json=self._categories_json[0])

        alias = "projects/1/taxonomy/categories"
        coll = CategoryCollection(self.unify, alias)

        creation_spec = {
            "name": self._categories_json[0]["name"],
            "path": self._categories_json[0]["path"],
        }
        c = coll.create(creation_spec)
        self.assertEqual(alias + "/1", c.relative_id)

    @responses.activate
    def test_bulk_create(self):
        def create_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, json.dumps(self._bulk_json)

        post_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories:bulk"
        )
        snoop_dict = {}
        responses.add_callback(
            responses.POST, post_url, partial(create_callback, snoop=snoop_dict)
        )

        alias = "projects/1/taxonomy/categories"
        coll = CategoryCollection(self.unify, alias)

        creation_specs = [
            {
                "name": self._categories_json[0]["name"],
                "path": self._categories_json[0]["path"],
            },
            {
                "name": self._categories_json[1]["name"],
                "path": self._categories_json[1]["path"],
            },
        ]
        j = coll.bulk_create(creation_specs)
        self.assertEqual(j, self._bulk_json)

        sent = []
        for line in snoop_dict["payload"].split(b"\n"):
            sent.append(json.loads(line))
        self.assertEqual(sent, creation_specs)

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

    _bulk_json = {
        "numCommandsProcessed": 2,
        "allCommandsSucceeded": True,
        "validationErrors": [],
    }
