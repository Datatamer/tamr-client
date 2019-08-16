from functools import partial
import json
from unittest import TestCase

from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.categorization.category.collection import CategoryCollection
from tamr_unify_client.categorization.category.resource import Category, CategorySpec
from tamr_unify_client.categorization.taxonomy import Taxonomy
from tamr_unify_client.project.resource import Project


class TestTaxonomy(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_categories(self):
        cat_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories"
        )
        responses.add(responses.GET, cat_url, json=self._categories_json)

        t = Taxonomy(self.tamr, self._taxonomy_json)
        c = list(t.categories())

        cats = [
            Category(self.tamr, self._categories_json[0]),
            Category(self.tamr, self._categories_json[1]),
        ]
        self.assertEqual(repr(c), repr(cats))

    @responses.activate
    def test_by_id(self):
        cat_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories/1"
        )
        responses.add(responses.GET, cat_url, json=self._categories_json[0])

        c = CategoryCollection(self.tamr, "projects/1/taxonomy/categories")
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
        coll = CategoryCollection(self.tamr, alias)

        creation_spec = {
            "name": self._categories_json[0]["name"],
            "path": self._categories_json[0]["path"],
        }
        c = coll.create(creation_spec)
        self.assertEqual(alias + "/1", c.relative_id)

    @responses.activate
    def test_create_from_spec(self):
        def create_callback(request, snoop):
            snoop["payload"] = json.loads(request.body)
            return 201, {}, json.dumps(self._categories_json[0])

        post_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories"
        )
        snoop_dict = {}
        responses.add_callback(
            responses.POST, post_url, partial(create_callback, snoop=snoop_dict)
        )

        alias = "projects/1/taxonomy/categories"
        coll = CategoryCollection(self.tamr, alias)

        json_spec = {
            "name": self._categories_json[0]["name"],
            "path": self._categories_json[0]["path"],
        }
        spec = (
            CategorySpec.new()
            .with_name(self._categories_json[0]["name"])
            .with_path(self._categories_json[0]["path"])
        )
        coll.create(spec.to_dict())

        self.assertEqual(snoop_dict["payload"], json_spec)

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
        coll = CategoryCollection(self.tamr, alias)

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

    @responses.activate
    def test_delete(self):
        url = "http://localhost:9100/api/versioned/v1/projects/1/taxonomy"
        responses.add(responses.GET, url, json=self._taxonomy_json)
        responses.add(responses.DELETE, url, status=204)
        responses.add(responses.GET, url, status=404)

        project = Project(
            self.tamr, {"type": "CATEGORIZATION"}, "projects/1"
        ).as_categorization()
        taxonomy = project.taxonomy()
        self.assertEqual(taxonomy._data, self._taxonomy_json)

        response = taxonomy.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(HTTPError, project.taxonomy)

    @responses.activate
    def test_delete_category(self):
        url = "http://localhost:9100/api/versioned/v1/projects/1/taxonomy/categories/1"
        responses.add(responses.GET, url, json=self._categories_json[0])
        responses.add(responses.DELETE, url, status=204)
        responses.add(responses.GET, url, status=404)

        categories = CategoryCollection(self.tamr, "projects/1/taxonomy/categories")
        category = categories.by_resource_id("1")
        self.assertEqual(category._data, self._categories_json[0])

        response = category.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(HTTPError, lambda: categories.by_resource_id("1"))

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
