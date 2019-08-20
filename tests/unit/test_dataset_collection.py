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
    ds_url = url_prefix + "datasets/115"

    responses.add(responses.DELETE, ds_url, status=204)

    response = client.datasets.delete_by_resource_id("115")
    assert response.status_code == 204


@responses.activate
def test_delete_by_resource_id_cascade(client):
    ds_url = url_prefix + "datasets/115?cascade=True"

    responses.add(responses.DELETE, ds_url, status=204)

    response = client.datasets.delete_by_resource_id("115", cascade=True)
    assert response.status_code == 204


url_prefix = "http://localhost:9100/api/versioned/v1/"
