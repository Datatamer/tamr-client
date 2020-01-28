from dataclasses import replace
import json
from pathlib import Path

from requests import Session
import responses

import tamr_unify_client as tc
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.dataset.resource import Dataset
from tests.utils import data_dir, load_json


def test_from_json():
    attrs_json = load_json(data_dir / "attributes.json")
    dataset_id = 1
    for attr_json in attrs_json:
        attr_id = attr_json["name"]
        url = tc.URL(
            path=f"api/versioned/v1/datasets/{dataset_id}/attributes/{attr_id}"
        )
        attr = tc.attribute._from_json(url, attr_json)
        assert attr.name == attr_json["name"]
        assert attr.description == attr_json["description"]
        assert attr.is_nullable == attr_json["isNullable"]


def test_json():
    """original -> to_json -> from_json -> original"""
    attrs_json = load_json(data_dir / "attributes.json")
    dataset_id = 1
    for attr_json in attrs_json:
        attr_id = attr_json["name"]
        url = tc.URL(f"api/versioned/v1/datasets/{dataset_id}/attributes/{attr_id}")
        attr = tc.attribute._from_json(url, attr_json)
        assert attr == tc.attribute._from_json(url, tc.attribute.to_json(attr))


@responses.activate
def test_create():
    attrs = tuple(
        [
            tc.SubAttribute(
                name=str(i),
                is_nullable=True,
                type=tc.attribute_type.Array(inner_type=tc.attribute_type.String()),
            )
            for i in range(4)
        ]
    )

    auth = UsernamePasswordAuth("username", "password")
    tamr = tc.Client(auth)
    dataset_json = load_json(data_dir / "dataset.json")
    dataset_url = tc.URL(path="api/versioned/v1/datasets/1")
    dataset = Dataset.from_json(tamr, dataset_json, api_path=dataset_url.path)

    url = tc.URL(path=dataset.url.path + "/attributes")
    attr_url = replace(url, path=url.path + "/attr")
    attr_json = load_json(data_dir / "attribute.json")
    responses.add(responses.POST, str(url), json=attr_json)
    attr = tc.attribute.create(
        Session(),
        dataset,
        name="attr",
        is_nullable=False,
        type=tc.attribute_type.Record(attributes=attrs),
    )

    assert attr == tc.attribute._from_json(attr_url, attr_json)


@responses.activate
def test_update():
    attr_url = tc.URL(path="api/versioned/v1/datasets/1/attributes/RowNum")
    attr_json = load_json(data_dir / "attributes.json")[0]
    attr = tc.attribute._from_json(attr_url, attr_json)

    updated_attr_json = load_json(data_dir / "updated_attribute.json")
    responses.add(responses.PUT, str(attr_url), json=updated_attr_json)
    updated_attr = tc.attribute.update(
        Session(), attr, description=updated_attr_json["description"]
    )

    assert updated_attr == replace(attr, description=updated_attr_json["description"])


@responses.activate
def test_delete():
    attr_url = tc.URL(path="api/versioned/v1/datasets/1/attributes/RowNum")
    attr_json = load_json(data_dir / "attributes.json")[0]
    attr = tc.attribute._from_json(attr_url, attr_json)

    responses.add(responses.DELETE, str(attr_url), status=204)
    tc.attribute.delete(Session(), attr)
