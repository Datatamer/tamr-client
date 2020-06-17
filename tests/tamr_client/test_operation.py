import responses

import tamr_client as tc
from tests.tamr_client import utils


def test_operation_from_json():
    url = tc.URL(path="operations/1")
    operation_json = utils.load_json("operation_succeeded.json")
    op = tc.operation._from_json(url, operation_json)
    assert op.url == url
    assert op.id == operation_json["id"]
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_from_url():
    s = utils.session()
    url = tc.URL(path="operations/1")

    operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=operation_json)

    op = tc.operation._from_url(s, url)
    assert op.url == url
    assert op.id == operation_json["id"]
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_from_response():
    s = utils.session()
    instance = utils.instance()
    url = tc.URL(path="operations/1")

    operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=operation_json)

    r = s.get(str(url))
    op = tc.operation.from_response(instance, r)
    assert op.url == url
    assert op.id == operation_json["id"]
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_poll():
    s = utils.session()
    url = tc.URL(path="operations/1")

    pending_operation_json = utils.load_json("operation_pending.json")
    op1 = tc.operation._from_json(url, pending_operation_json)

    succeeded_operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=succeeded_operation_json)
    op2 = tc.operation.poll(s, op1)

    assert op2.id == op1.id
    assert not tc.operation.succeeded(op1)
    assert tc.operation.succeeded(op2)
