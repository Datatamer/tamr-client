"""
Utilities for faking Tamr resources and server responses for testing.

For more, see "How to write tests" in the Contributor guide.
"""

from functools import partial, wraps
from inspect import getfile
from json import dumps, load, loads
from pathlib import Path

import responses

import tamr_client as tc


tests_tc_dir = (Path(__file__) / "..").resolve()
fake_json_dir = tests_tc_dir / "fake_json"


class WrongRequestBody(Exception):
    """Raised when the body of a request does not match the value expected during
    testing
    """

    pass


def check_request_body(request, request_body, status, response_json):
    if isinstance(request_body, list):
        caught_body = [loads(x.decode("utf-8")) for x in request.body]
        if caught_body != request_body:
            raise WrongRequestBody(caught_body)
    elif request_body is not None:
        caught_body = loads(request.body.decode("utf-8"))
        if caught_body != request_body:
            raise WrongRequestBody(caught_body)
    return status, {}, response_json


def add_response(rsps, fake):
    req = fake["request"]
    resp = fake["response"]

    url = req.get("url")
    if url is None:
        path = req.get("path")
        url = "http://localhost/api/versioned/v1/" + path

    # Get response body from either ndjson or json
    if resp.get("ndjson") is not None:
        resp["body"] = "\n".join((dumps(line) for line in resp["ndjson"]))
    elif resp.get("json") is not None:
        resp["body"] = dumps(resp["json"])

    # Get expected request body from ndjson
    if req.get("ndjson") is not None:
        req["body"] = [x for x in req["ndjson"]]
    elif req.get("json") is not None:
        req["body"] = req["json"]

    rsps.add_callback(
        method=req["method"],
        url=url,
        callback=partial(
            check_request_body,
            request_body=req.get("body"),
            status=resp["status"],
            response_json=resp.get("body"),
        ),
    )


def json(test_fn):
    """Intercept API requests and respond with fake JSON data.

    Will look in fake_json directory for data corresponding to the decorated test.
    Data format is a JSON list of request/response pairs in order of execution.
    """
    test_file = Path(getfile(test_fn))

    fakes_mod_path = fake_json_dir / test_file.relative_to(tests_tc_dir).with_suffix("")
    fakes_test_path = (fakes_mod_path / test_fn.__name__).with_suffix(".json")
    with open(fakes_test_path) as f:
        fakes = load(f)

    @wraps(test_fn)
    def wrapper(*args, **kwargs):
        with responses.RequestsMock() as rsps:
            for fake in fakes:
                add_response(rsps, fake)
            test_fn(*args, **kwargs)

    return wrapper


def session() -> tc.Session:
    auth = tc.UsernamePasswordAuth("username", "password")
    s = tc.session.from_auth(auth)
    return s


def instance() -> tc.Instance:
    return tc.Instance()


def dataset() -> tc.Dataset:
    url = tc.URL(path="datasets/1")
    dataset = tc.Dataset(url, name="dataset.csv", key_attribute_names=("primary_key",))
    return dataset


def unified_dataset() -> tc.UnifiedDataset:
    url = tc.URL(path="projects/1/unifiedDataset")
    unified_dataset = tc.dataset.unified.UnifiedDataset(
        url, name="dataset.csv", key_attribute_names=("primary_key",)
    )
    return unified_dataset


def mastering_project() -> tc.MasteringProject:
    url = tc.URL(path="projects/1")
    mastering_project = tc.MasteringProject(
        url, name="Project 1", description="A Mastering Project"
    )
    return mastering_project


def categorization_project() -> tc.CategorizationProject:
    url = tc.URL(path="projects/2")
    categorization_project = tc.CategorizationProject(
        url, name="Project 2", description="A Categorization Project"
    )
    return categorization_project


def transforms() -> tc.Transformations:
    return tc.Transformations(
        input_scope=[
            tc.InputTransformation("SELECT *, 1 as one;"),
            tc.InputTransformation("SELECT *, 2 as two;", datasets=[dataset()]),
        ],
        unified_scope=["//Comment\nSELECT *;"],
    )


def attribute() -> tc.Attribute:
    return tc.Attribute(
        url=tc.URL(path="datasets/1/attributes/RowNum"),
        name="RowNum",
        type=tc.attribute.type.DEFAULT,
        description="Synthetic row number",
        is_nullable=False,
    )
