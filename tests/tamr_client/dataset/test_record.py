from functools import partial
from typing import Dict

import pytest
import responses

import tamr_client as tc
from tests.tamr_client import fake, utils


@responses.activate
def test_update():
    s = fake.session()
    dataset = fake.dataset()

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


@fake.json
def test_upsert():
    s = fake.session()
    dataset = fake.dataset()

    response = tc.record.upsert(
        s, dataset, _records_json, primary_key_name="primary_key"
    )
    assert response == _response_json


@responses.activate
def test_upsert_primary_key_not_found():
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.primary_key.NotFound):
        tc.record.upsert(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


@responses.activate
def test_upsert_infer_primary_key():
    s = fake.session()
    dataset = fake.dataset()

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
    s = fake.session()
    dataset = fake.dataset()

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
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.primary_key.NotFound):
        tc.record.delete(
            s, dataset, _records_json, primary_key_name="wrong_primary_key"
        )


@responses.activate
def test_delete_infer_primary_key():
    s = fake.session()
    dataset = fake.dataset()

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


@fake.json
def test_stream():
    s = fake.session()
    dataset = fake.dataset()

    records = tc.record.stream(s, dataset)
    assert list(records) == _records_json


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
