import json

import responses

import tamr_client as tc
import tests.tamr_client.utils as utils


@responses.activate
def test_ndjson():
    s = utils.session()

    records = [{"a": 1}, {"b": 2}, {"c": 3}]
    url = tc.URL(path="datasets/1/records")
    responses.add(
        responses.GET, str(url), body="\n".join(json.dumps(x) for x in records)
    )

    r = s.get(str(url))

    ndjson = list(tc.response.ndjson(r))
    assert len(ndjson) == 3
    for record in ndjson:
        assert record in records
