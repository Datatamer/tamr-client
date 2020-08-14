"""
Utilities for faking Tamr resources and server responses for testing.

For more, see "How to write tests" in the Contributor guide.
"""

from functools import partial, wraps
from inspect import getfile
from json import dumps, load
from pathlib import Path

import responses

import tamr_client as tc


tests_tc_dir = (Path(__file__) / "..").resolve()
fake_json_dir = tests_tc_dir / "fake_json"


def check_payload(request, correct_payload, status, response_json):
    if correct_payload is not None:
        if [x.decode("utf-8") for x in request.body] != correct_payload:
            raise Exception("placeholder exception")
    return status, {}, response_json


def add_response(rsps, fake):
    req = fake["request"]
    resp = fake["response"]

    url = req.get("url")
    if url is None:
        path = req.get("path")
        url = "http://localhost/api/versioned/v1/" + path

    ndjson = resp.pop("ndjson", None)
    if ndjson is not None:
        resp["body"] = "\n".join((dumps(line) for line in ndjson))

    payload = req.pop("payload", None)
    callback = partial(
        check_payload,
        correct_payload=[dumps(x) for x in payload] if payload is not None else None,
        status=resp.get("status", 200),  # TODO: Every response needs a status
        response_json=resp.get("body") or dumps(resp.get("json")),
    )

    rsps.add_callback(
        method=req["method"],
        url=url,
        callback=callback,
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
