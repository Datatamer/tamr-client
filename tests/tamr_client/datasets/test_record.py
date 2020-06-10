from functools import partial
import json
from typing import Dict

import pytest
import responses

import tamr_client as tc
from tests.tamr_client import utils


@responses.activate
def test_update():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = [
        tc.record._create_command(record, primary_key_name="primary_key")
        for record in _records_json
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    response = tc.record._update(s, dataset, updates)
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(updates)


@responses.activate
def test_upsert():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = [
        tc.record._create_command(record, primary_key_name="primary_key")
        for record in _records_json
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    response = tc.record.upsert(
        s, dataset, _records_json, primary_key_name="primary_key"
    )
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(updates)


@responses.activate
def test_upsert_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.record.upsert(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


@responses.activate
def test_upsert_infer_primary_key():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = [
        tc.record._create_command(record, primary_key_name="primary_key")
        for record in _records_json
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    response = tc.record.upsert(s, dataset, _records_json)
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(updates)


@responses.activate
def test_delete():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = [
        tc.record._delete_command(record, primary_key_name="primary_key")
        for record in _records_json
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    response = tc.record.delete(
        s, dataset, _records_json, primary_key_name="primary_key"
    )
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(deletes)


@responses.activate
def test_delete_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.record.delete(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


@responses.activate
def test_delete_infer_primary_key():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = [
        tc.record._delete_command(record, primary_key_name="primary_key")
        for record in _records_json
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    response = tc.record.delete(s, dataset, _records_json)
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(deletes)


@responses.activate
def test_stream():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1/records")
    responses.add(
        responses.GET, str(url), body="\n".join(json.dumps(x) for x in _records_json)
    )

    records = tc.record.stream(s, dataset)
    assert list(records) == _records_json


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
