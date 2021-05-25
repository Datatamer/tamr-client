"""
Utilities for faking Tamr resources and server responses for testing.

For more, see "How to write tests" in the Contributor guide.
"""

from functools import partial, wraps
from inspect import getfile
from json import dumps, load, loads
from pathlib import Path
from typing import Dict, Tuple

import responses

import tamr_client as tc
from tamr_client._types import JsonDict


tests_tc_dir = (Path(__file__) / "..").resolve()
fake_json_dir = tests_tc_dir / "fake_json"


class WrongRequestBody(Exception):
    """Raised when the body of a request does not match the value expected during
    testing
    """

    pass


def _check_request_body(request, expected_body: JsonDict):
    """Checks that the body of a caught request matches the expected content

    The body is decoded and loaded as a JSON object so the comparison is not sensitive to the
    order of dictionary contents.  The comparison is sensitive to the order of a newline-delimited
    JSON request body.

    Args:
        request: The caught request
        expected_body: The expected request body as a dictionary (for JSON contents) or a list of
            dictionaries (for newline-delimited JSON contents)
    """
    if isinstance(expected_body, list):
        actual_body = [loads(x.decode("utf-8")) for x in request.body]
        if actual_body != expected_body:
            raise WrongRequestBody(actual_body)
    elif expected_body is not None:
        actual_body = loads(request.body.decode("utf-8"))
        if actual_body != expected_body:
            raise WrongRequestBody(actual_body)


def _callback(
    request, expected_body: JsonDict, status: int, response_json: str
) -> Tuple[int, Dict, str]:
    """Adds a callback to intercept an API request, check the validity of the request, and emit a
    response

    Args:
        expected_body: The expected request body as a dictionary (for JSON contents) or a list of
            dictionaries (for newline-delimited JSON contents)
        status: The status of the response to be emitted
        response_json: The JSON body of the response to be emitted

    Returns:
        Response status, headers, and JSON body.  This conforms to the callback interface of
            `~responses.RequestsMock.add_callback`
    """
    _check_request_body(request, expected_body)
    return status, {}, response_json


def add_response(rsps, fake: JsonDict):
    """Adds a mock response to intercept API requests and respond with fake JSON data

    Args:
        fake: The JSON dictionary containing the fake data defining what requests to intercept and
            what responses to emit
    """
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
        req["body"] = req["ndjson"]
    elif req.get("json") is not None:
        req["body"] = req["json"]

    rsps.add_callback(
        method=req["method"],
        url=url,
        callback=partial(
            _callback,
            expected_body=req.get("body"),
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


def username_password_auth() -> tc.UsernamePasswordAuth:
    return tc.UsernamePasswordAuth("username", "password")


def session() -> tc._types.Session:
    auth = username_password_auth()
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


def golden_records_project() -> tc.GoldenRecordsProject:
    url = tc.URL(path="projects/3")
    golden_records_project = tc.GoldenRecordsProject(
        url, name="Project 3", description="A Golden Records Project"
    )
    return golden_records_project


def schema_mapping_project() -> tc.SchemaMappingProject:
    url = tc.URL(path="projects/4")
    schema_mapping_project = tc.SchemaMappingProject(
        url, name="Project 4", description="A Schema Mapping Project"
    )
    return schema_mapping_project


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


def attribute_mapping() -> tc.AttributeMapping:
    return tc.AttributeMapping(
        url=tc.URL(path="projects/4/attributeMappings/123-456"),
        input_attribute=attribute(),
        unified_attribute=tc.Attribute(
            url=tc.URL(path="datasets/2/attributes/SourceRowNum"),
            name="RowNum",
            type=tc.attribute.type.DEFAULT,
            description="Synthetic row number",
            is_nullable=False,
        ),
    )


def project_attribute() -> tc.Attribute:
    return tc.Attribute(
        url=tc.URL(path="projects/1/attributes/StreetAddress"),
        name="StreetAddress",
        type=tc.attribute.type.DEFAULT,
        description="A Mastering Project attribute",
        is_nullable=False,
    )


def attribute_configuration() -> tc.AttributeConfiguration:
    return tc.AttributeConfiguration(
        url=tc.URL(path="projects/1/attributeConfigurations/1600"),
        attribute=project_attribute(),
        attribute_role=tc.attribute.configuration.AttributeRole.NONE,
        similarity_function=tc.attribute.configuration.SimilarityFunction.COSINE,
        enabled_for_ml=True,
        tokenizer=tc.attribute.configuration.Tokenizer.DEFAULT,
        numeric_field_resolution=[],
    )
