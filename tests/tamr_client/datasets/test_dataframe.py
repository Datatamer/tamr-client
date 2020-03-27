from functools import partial
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
    updates = [
        tc.record._create_command(record, primary_key_name="primary_key")
        for i, record in enumerate(_records_json, start=1)
    ]
    snoop: Dict = {}
    responses.add_callback(
        responses.POST,
        str(url),
        partial(
            utils.capture_payload, snoop=snoop, status=200, response_json=_response_json
        ),
    )

    df = pd.DataFrame(_records_json)

    response = tc.dataframe.upsert(s, dataset, df, primary_key_name="primary_key")
    assert response == _response_json
    assert snoop["payload"] == utils.stringify(updates)


@responses.activate
def test_upsert_primary_key_not_found():
    s = utils.session()
    dataset = utils.dataset()

    df = pd.DataFrame(_records_json)

    with pytest.raises(tc.record.PrimaryKeyNotFound):
        tc.dataframe.upsert(s, dataset, df, primary_key_name="wrong_primary_key")


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
