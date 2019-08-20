import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attribute_mapping.resource import AttributeMapping


@pytest.fixture
def client():

    return Client(UsernamePasswordAuth("username", "password"))


def test_resource(client):
    test = AttributeMapping(client, mappings_json)

    expected = mappings_json["relativeId"]
    assert expected == test.relative_id

    expected = mappings_json["id"]
    assert expected == test.id

    expected = mappings_json["inputAttributeId"]
    assert expected == test.input_attribute_id

    expected = mappings_json["relativeInputAttributeId"]
    assert expected == test.relative_input_attribute_id

    expected = mappings_json["inputDatasetName"]
    assert expected == test.input_dataset_name

    expected = mappings_json["inputAttributeName"]
    assert expected == test.input_attribute_name

    expected = mappings_json["unifiedAttributeId"]
    assert expected == test.unified_attribute_id

    expected = mappings_json["relativeUnifiedAttributeId"]
    assert expected == test.relative_unified_attribute_id

    expected = mappings_json["unifiedDatasetName"]
    assert expected == test.unified_dataset_name

    expected = mappings_json["unifiedAttributeName"]
    assert expected == test.unified_attribute_name


@responses.activate
def test_delete(client):
    specific_url = (
        "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings/19629-12"
    )
    responses.add(responses.DELETE, specific_url, status=204)
    delete_map = AttributeMapping(client, mappings_json)
    final_response = delete_map.delete()
    assert final_response.status_code == 204


mappings_json = {
    "id": "unify://unified-data/v1/projects/4/attributeMappings/19629-12",
    "relativeId": "projects/4/attributeMappings/19629-12",
    "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/surname",
    "relativeInputAttributeId": "datasets/6/attributes/surname",
    "inputDatasetName": "febrl_sample_2k.csv",
    "inputAttributeName": "surname",
    "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/surname",
    "relativeUnifiedAttributeId": "datasets/79/attributes/surname",
    "unifiedDatasetName": "Charlotte_unified_dataset",
    "unifiedAttributeName": "surname",
}
