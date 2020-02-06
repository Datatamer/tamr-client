from dataclasses import replace

import responses

import tamr_client as tc
import tests.utils as utils


@responses.activate
def test_attributes():
    s = utils.session()
    dataset = utils.dataset()

    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    attrs_json = utils.load_json("attributes.json")
    responses.add(responses.GET, str(attrs_url), json=attrs_json, status=204)

    attrs = tc.dataset.attributes(s, dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert isinstance(row_num.type, tc.attribute_type.String)

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute_type.Record)
