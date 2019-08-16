from functools import partial
import json

from pandas import DataFrame
import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.dataset.collection import CreationError
from tamr_unify_client.dataset.resource import DatasetSpec

auth = UsernamePasswordAuth("username", "password")
tamr = Client(auth)


@responses.activate
def test_create_dataset():
    def create_callback(request, snoop):
        snoop["payload"] = json.loads(request.body)
        return 201, {}, json.dumps(_dataset_json)

    dataset_url = _datasets_url + "/1"
    snoop_dict = {}
    responses.add_callback(
        responses.POST, _datasets_url, partial(create_callback, snoop=snoop_dict)
    )
    responses.add(responses.GET, dataset_url, json=_dataset_json)

    u = tamr.datasets.create(_creation_spec)
    p = tamr.datasets.by_resource_id("1")

    assert u.name == p.name
    assert u.key_attribute_names == p.key_attribute_names
    assert u.description == p.description
    assert u.external_id == p.external_id


@responses.activate
def test_create_from_dataframe():
    def create_callback(request, snoop):
        snoop["creation"] = json.loads(request.body)
        return 201, {}, json.dumps(_dataset_json)

    def attribute_callback(request, snoop):
        snoop["attribute"] = json.loads(request.body)
        return 201, {}, json.dumps(_attribute_json)

    def record_callback(request, snoop):
        snoop["records"] = [json.loads(r) for r in request.body]
        return 200, {}, json.dumps(_records_response_json)

    snoop_dict = {}
    responses.add_callback(
        responses.POST, _datasets_url, partial(create_callback, snoop=snoop_dict)
    )
    responses.add_callback(
        responses.POST, _attribute_url, partial(attribute_callback, snoop=snoop_dict)
    )
    # only one additional attribute should be created, as the pk is handled at dataset creation
    responses.add(responses.POST, _attribute_url, status=500)
    responses.add_callback(
        responses.POST, _records_url, partial(record_callback, snoop=snoop_dict)
    )

    dataset = tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")
    assert dataset.name == _dataset_json["name"]

    creation_spec = snoop_dict["creation"]
    assert creation_spec["name"] == _dataset_json["name"]
    assert creation_spec["keyAttributeNames"], ["attribute1"]

    attribute_spec = snoop_dict["attribute"]
    assert attribute_spec["name"] == _attribute_json["name"]
    assert attribute_spec["type"] == _attribute_json["type"]

    records_spec = snoop_dict["records"]
    assert len(records_spec) == len(_records_json)
    for command, record in zip(records_spec, _records_json):
        assert command["action"] == "CREATE"
        assert command["record"] == record


def test_key_not_in_dataframe():
    with pytest.raises(KeyError):
        tamr.datasets.create_from_dataframe(_dataframe, "bad key", "Dataset")


@responses.activate
def test_creation_initial_failure():
    responses.add(responses.POST, _datasets_url, status=500)
    responses.add(responses.DELETE, _datasets_url + "/1", status=204)

    with pytest.raises(CreationError):
        tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")


@responses.activate
def test_attribute_creation_failure():
    responses.add(responses.POST, _datasets_url, json=_dataset_json)
    responses.add(responses.POST, _attribute_url, status=500)
    responses.add(responses.DELETE, _dataset_url, status=204)

    with pytest.raises(CreationError):
        tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")


@responses.activate
def test_record_failure():
    responses.add(responses.POST, _datasets_url, json=_dataset_json)
    responses.add(responses.POST, _attribute_url, json=_attribute_json)
    responses.add(responses.POST, _records_url, status=500)
    responses.add(responses.DELETE, _dataset_url, status=204)

    with pytest.raises(CreationError):
        tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")


@responses.activate
def test_record_validation_failure():
    responses.add(responses.POST, _datasets_url, json=_dataset_json)
    responses.add(responses.POST, _attribute_url, json=_attribute_json)
    responses.add(responses.POST, _records_url, json=_records_failure_json)
    responses.add(responses.DELETE, _dataset_url, status=204)

    with pytest.raises(CreationError):
        tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")


@responses.activate
def test_dataset_deletion_failure():
    responses.add(responses.POST, _datasets_url, json=_dataset_json)
    responses.add(responses.POST, _attribute_url, json=_attribute_json)
    responses.add(responses.POST, _records_url, json=_records_failure_json)
    responses.add(responses.DELETE, _dataset_url, status=500)

    with pytest.raises(CreationError):
        tamr.datasets.create_from_dataframe(_dataframe, "attribute1", "Dataset")


@responses.activate
def test_create_from_spec():
    def create_callback(request, snoop):
        snoop["payload"] = json.loads(request.body)
        return 201, {}, json.dumps(_dataset_json)

    snoop_dict = {}
    responses.add_callback(
        responses.POST, _datasets_url, partial(create_callback, snoop=snoop_dict)
    )

    spec = (
        DatasetSpec.new()
        .with_name(_creation_spec["name"])
        .with_key_attribute_names(_creation_spec["keyAttributeNames"])
        .with_description(_creation_spec["description"])
        .with_external_id(_creation_spec["externalId"])
    )
    d = tamr.datasets.create(spec.to_dict())

    assert snoop_dict["payload"] == _creation_spec
    assert d.relative_id == _dataset_json["relativeId"]


_creation_spec = {
    "name": "Dataset",
    "keyAttributeNames": ["F1"],
    "description": "So much data in here!",
    "externalId": "Dataset created with pubapi",
}

_datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"
_dataset_url = _datasets_url + "/1"
_attribute_url = _dataset_url + "/attributes"
_records_url = _dataset_url + ":updateRecords"

_records_json = [
    {"attribute1": 1, "attribute2": "hi"},
    {"attribute1": 2, "attribute2": "record"},
]
_dataframe = DataFrame(_records_json, columns=["attribute1", "attribute2"])

_records_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}

_records_failure_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": False,
    "validationErrors": [],
}

_dataset_json = {
    **_creation_spec,
    "id": "unify://unified-data/v1/datasets/1",
    "version": "1",
    "tags": [],
    "created": {
        "username": "admin",
        "time": "2018-09-10T16:06:20.636Z",
        "version": "1",
    },
    "lastModified": {
        "username": "admin",
        "time": "2018-09-10T16:06:20.636Z",
        "version": "1",
    },
    "relativeId": "datasets/1",
    "upstreamDatasetIds": [],
}

_attribute_json = {
    "name": "attribute2",
    "description": "",
    "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
    "isNullable": False,
}
