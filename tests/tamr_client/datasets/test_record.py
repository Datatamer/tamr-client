from functools import partial
import json
from typing import Dict

import pytest
import responses

import tamr_client as tc
import tests.tamr_client.utils as utils


@responses.activate
def test_update():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = _records_to_updates(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST, str(url), partial(capture_payload, snoop=snoop, status=200)
    )

    response = tc.record._update(s, dataset, updates)
    assert response == _response_json
    assert snoop["payload"] == _stringify(updates)


@responses.activate
def test_upsert():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = _records_to_updates(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST, str(url), partial(capture_payload, snoop=snoop, status=200)
    )

    response = tc.record.upsert(
        s, dataset, _records_json, primary_key_name="primary_key"
    )
    assert response == _response_json
    assert snoop["payload"] == _stringify(updates)


@responses.activate
def test_upsert_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.record.upsert(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


@responses.activate
def test_delete_by_ids():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = _records_to_deletes(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST, str(url), partial(capture_payload, snoop=snoop, status=200)
    )

    ids = (r["primary_key"] for r in _records_json)

    response = tc.record._delete_by_id(s, dataset, ids)
    assert response == _response_json
    assert snoop["payload"] == _stringify(deletes)


@responses.activate
def test_delete():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = _records_to_deletes(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST, str(url), partial(capture_payload, snoop=snoop, status=200)
    )

    response = tc.record.delete(
        s, dataset, _records_json, primary_key_name="primary_key"
    )
    assert response == _response_json
    assert snoop["payload"] == _stringify(deletes)


@responses.activate
def test_delete_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.record.delete(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


def capture_payload(request, snoop, status):
    snoop["payload"] = list(request.body)
    return status, {}, json.dumps(_response_json)


def _records_to_deletes(records):
    return [
        {"action": "DELETE", "recordId": i} for i, record in enumerate(records, start=1)
    ]


def _records_to_updates(records):
    return [
        {"action": "CREATE", "recordId": i, "record": record}
        for i, record in enumerate(records, start=1)
    ]


def _stringify(updates):
    return [json.dumps(u) for u in updates]


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
