from dataclasses import replace

from requests import Session
import responses

import tamr_unify_client as tc
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.dataset.resource import Dataset
from tests.utils import data_dir, load_json


@responses.activate
def test__attributes():
    auth = UsernamePasswordAuth("username", "password")
    tamr = tc.Client(auth)
    dataset_json = load_json(data_dir / "dataset.json")
    dataset_url = tc.URL(path="api/versioned/v1/datasets/1")
    dataset = Dataset.from_json(tamr, dataset_json, api_path=dataset_url.path)

    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    attrs_json = load_json(data_dir / "attributes.json")
    responses.add(responses.GET, str(attrs_url), json=attrs_json, status=204)

    attrs = tc.dataset._attributes(Session(), dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert isinstance(row_num.type, tc.attribute_type.String)

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute_type.Record)
