import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@pytest.fixture
def client():
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    return tamr


@responses.activate
def test_delete_by_resource_id(client):
    taxonomy_url = categorization_project + "/taxonomy"
    category_url = taxonomy_url + "/categories/3"

    responses.add(
        responses.GET, categorization_project, json=categorization_project_config
    )

    responses.add(responses.GET, taxonomy_url, json=taxonomy)
    responses.add(responses.DELETE, category_url, status=204)

    category_collection = client.projects.by_resource_id("2").as_categorization()
    response = category_collection.taxonomy().categories().delete_by_resource_id("3")
    assert response.status_code == 204


url_prefix = "http://localhost:9100/api/versioned/v1/"
categorization_project = url_prefix + "projects/2"

categorization_project_config = {
    "id": "unify://unified-data/v1/projects/2",
    "name": "cat",
    "description": "Categorization Project",
    "type": "CATEGORIZATION",
    "unifiedDatasetName": "",
    "relativeId": "projects/2",
    "externalId": "904bf89e-74ba-45c5-8b4a-5ff913728f66",
}

taxonomy = {
    "id": "unify://unified-data/v1/projects/2/taxonomy",
    "name": "tax",
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
    "relativeId": "projects/2/taxonomy",
}
