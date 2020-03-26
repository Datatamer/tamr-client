from functools import partial
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
    updates = utils.records_to_updates(_records_json)
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
    updates = utils.records_to_updates(_records_json)
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
def test_delete_by_ids():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = utils.records_to_deletes(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    ids = (r["primary_key"] for r in _records_json)

    response = tc.record._delete_by_id(s, dataset, ids)
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(deletes)


@responses.activate
def test_delete():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    deletes = utils.records_to_deletes(_records_json)
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


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
