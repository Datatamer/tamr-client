from functools import partial
import json
from typing import Dict

import pandas as pd
import pytest
import responses

import tamr_client as tc
import tests.tamr_client.utils as utils


@responses.activate
def test_upsert():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path="datasets/1:updateRecords")
    updates = _records_to_updates(_records_json)
    snoop: Dict = {}
    responses.add_callback(
        responses.POST, str(url), partial(_capture_payload, snoop=snoop, status=200)
    )

    df = pd.DataFrame(_records_json)

    response = tc.dataframe.upsert(s, dataset, df, primary_key_name="primary_key")
    assert response == _response_json
    assert snoop["payload"] == _stringify(updates)


@responses.activate
def test_upsert_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    df = pd.DataFrame(_records_json)

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.dataframe.upsert(s, dataset, df, primary_key_name="wrong_primary_key")


def _capture_payload(request, snoop, status):
    """Capture request body within `snoop` so we can inspect that the request body is constructed correctly (e.g. for streaming requests).

    See https://github.com/getsentry/responses#dynamic-responses
    """
    snoop["payload"] = list(request.body)
    return status, {}, json.dumps(_response_json)


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
