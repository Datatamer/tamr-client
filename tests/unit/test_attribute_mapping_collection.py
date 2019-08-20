from functools import partial
import json

import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attribute_mapping.collection import (
    AttributeMappingCollection,
)
from tamr_unify_client.project.attribute_mapping.resource import AttributeMappingSpec


@pytest.fixture
def client():
    return Client(UsernamePasswordAuth("username", "password"))


@responses.activate
def test_by_resource_id(client):
    url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
    responses.add(responses.GET, url, json=mappings_json)
    tester = AttributeMappingCollection(client, url)
    by_resource = tester.by_resource_id("19629-12")
    assert (
        by_resource.unified_attribute_name == mappings_json[0]["unifiedAttributeName"]
    )


@responses.activate
def test_by_relative_id(client):
    url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
    responses.add(responses.GET, url, json=mappings_json)
    tester = AttributeMappingCollection(client, url)
    by_relative = tester.by_relative_id("projects/4/attributeMappings/19629-12")
    assert (
        by_relative.unified_attribute_name == mappings_json[0]["unifiedAttributeName"]
    )


@responses.activate
def test_create(client):
    def create_callback(request, snoop):
        snoop["payload"] = request.body
        return 200, {}, json.dumps(mappings_json[0])

    url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
    responses.add(responses.GET, url, json=mappings_json)
    snoop_dict = {}
    responses.add_callback(
        responses.POST, url, partial(create_callback, snoop=snoop_dict)
    )
    map_collection = AttributeMappingCollection(client, "projects/4/attributeMappings")
    test = map_collection.create(create_json)
    assert test.input_dataset_name == create_json["inputDatasetName"]
    assert json.loads(snoop_dict["payload"]) == create_json


@responses.activate
def test_delete(client):
    general_url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
    delete_collection = AttributeMappingCollection(client, general_url)
    specific_url = general_url + "/19629-12"
    responses.add(responses.DELETE, specific_url, status=204)
    response = delete_collection.delete_by_resource_id("19629-12")
    assert response.status_code == 204


@responses.activate
def test_create_from_spec(client):
    def create_callback(request, snoop):
        snoop["payload"] = json.loads(request.body)
        return 200, {}, json.dumps(mappings_json[0])

    url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
    responses.add(responses.GET, url, json=mappings_json)
    snoop_dict = {}
    responses.add_callback(
        responses.POST, url, partial(create_callback, snoop=snoop_dict)
    )

    map_collection = AttributeMappingCollection(client, "projects/4/attributeMappings")
    spec = (
        AttributeMappingSpec.new()
        .with_relative_input_attribute_id(create_json["relativeInputAttributeId"])
        .with_input_dataset_name(create_json["inputDatasetName"])
        .with_input_attribute_name(create_json["inputAttributeName"])
        .with_relative_unified_attribute_id(create_json["relativeUnifiedAttributeId"])
        .with_unified_dataset_name(create_json["unifiedDatasetName"])
        .with_unified_attribute_name(create_json["unifiedAttributeName"])
    )
    map_collection.create(spec.to_dict())

    assert snoop_dict["payload"] == create_json
    map_collection = AttributeMappingCollection(client, "projects/4/attributeMappings")
    test = map_collection.create(create_json)
    assert test.input_dataset_name == create_json["inputDatasetName"]
    assert snoop_dict["payload"] == create_json


create_json = {
    "relativeInputAttributeId": "datasets/6/attributes/suburb",
    "inputDatasetName": "febrl_sample_2k.csv",
    "inputAttributeName": "suburb",
    "relativeUnifiedAttributeId": "datasets/8/attributes/suburb",
    "unifiedDatasetName": "Project_1_unified_dataset",
    "unifiedAttributeName": "suburb",
}

created_json = {
    **create_json,
    "id": "unify://unified-data/v1/projects/1/attributeMappings/19594-14",
    "relativeId": "projects/1/attributeMappings/19594-14",
    "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/suburb",
    "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/suburb",
}

mappings_json = [
    {
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
    },
    {
        "id": "unify://unified-data/v1/projects/4/attributeMappings/19629-17",
        "relativeId": "projects/4/attributeMappings/19629-17",
        "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_1",
        "relativeInputAttributeId": "datasets/6/attributes/address_1",
        "inputDatasetName": "febrl_sample_2k.csv",
        "inputAttributeName": "address_1",
        "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/surname",
        "relativeUnifiedAttributeId": "datasets/79/attributes/surname",
        "unifiedDatasetName": "Charlotte_unified_dataset",
        "unifiedAttributeName": "surname",
    },
    {
        "id": "unify://unified-data/v1/projects/4/attributeMappings/19630-16",
        "relativeId": "projects/4/attributeMappings/19630-16",
        "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/street_number",
        "relativeInputAttributeId": "datasets/6/attributes/street_number",
        "inputDatasetName": "febrl_sample_2k.csv",
        "inputAttributeName": "street_number",
        "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/street_number",
        "relativeUnifiedAttributeId": "datasets/79/attributes/street_number",
        "unifiedDatasetName": "Charlotte_unified_dataset",
        "unifiedAttributeName": "street_number",
    },
    {
        "id": "unify://unified-data/v1/projects/4/attributeMappings/19631-17",
        "relativeId": "projects/4/attributeMappings/19631-17",
        "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_1",
        "relativeInputAttributeId": "datasets/6/attributes/address_1",
        "inputDatasetName": "febrl_sample_2k.csv",
        "inputAttributeName": "address_1",
        "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/address_1",
        "relativeUnifiedAttributeId": "datasets/79/attributes/address_1",
        "unifiedDatasetName": "Charlotte_unified_dataset",
        "unifiedAttributeName": "address_1",
    },
    {
        "id": "unify://unified-data/v1/projects/4/attributeMappings/19632-9",
        "relativeId": "projects/4/attributeMappings/19632-9",
        "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/date_of_birth",
        "relativeInputAttributeId": "datasets/6/attributes/date_of_birth",
        "inputDatasetName": "febrl_sample_2k.csv",
        "inputAttributeName": "date_of_birth",
        "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/Birthday",
        "relativeUnifiedAttributeId": "datasets/79/attributes/Birthday",
        "unifiedDatasetName": "Charlotte_unified_dataset",
        "unifiedAttributeName": "Birthday",
    },
]
