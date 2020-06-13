import json
from pathlib import Path
from typing import Union

import tamr_client as tc

data_dir = Path(__file__).parent / "data"


def load_json(path: Union[str, Path]):
    with open(data_dir / path) as f:
        return json.load(f)


def session():
    auth = tc.UsernamePasswordAuth("username", "password")
    s = tc.session.from_auth(auth)
    return s


def instance():
    return tc.Instance()


def dataset():
    url = tc.URL(path="datasets/1")
    dataset = tc.Dataset(url, name="dataset.csv", key_attribute_names=("primary_key",))
    return dataset


def unified_dataset():
    url = tc.URL(path="projects/1/unifiedDataset")
    unified_dataset = tc.unified.Dataset(url, name="dataset.csv", key_attribute_names=("primary_key",))
    return unified_dataset


def mastering_project():
    url = tc.URL(path="projects/1")
    mastering_project = tc.mastering.Project(url, name="Project 1", description="A Mastering Project")
    return mastering_project


def capture_payload(request, snoop, status, response_json):
    """Capture request body within `snoop` so we can inspect that the request body is constructed correctly (e.g. for streaming requests).

    See https://github.com/getsentry/responses#dynamic-responses
    """
    snoop["payload"] = list(request.body)
    return status, {}, json.dumps(response_json)


def stringify(updates):
    return [json.dumps(u) for u in updates]
