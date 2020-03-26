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


def capture_payload(request, snoop, status, response_json):
    """Capture request body within `snoop` so we can inspect that the request body is constructed correctly (e.g. for streaming requests).

    See https://github.com/getsentry/responses#dynamic-responses
    """
    snoop["payload"] = list(request.body)
    return status, {}, json.dumps(response_json)


def records_to_deletes(records):
    return [
        {"action": "DELETE", "recordId": i} for i, record in enumerate(records, start=1)
    ]


def records_to_updates(records):
    return [
        {"action": "CREATE", "recordId": i, "record": record}
        for i, record in enumerate(records, start=1)
    ]


def stringify(updates):
    return [json.dumps(u) for u in updates]
