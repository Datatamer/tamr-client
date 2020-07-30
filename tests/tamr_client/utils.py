import json
from pathlib import Path
from typing import Union


data_dir = Path(__file__).parent / "data"


def load_json(path: Union[str, Path]):
    with open(data_dir / path) as f:
        return json.load(f)


def capture_payload(request, snoop, status, response_json):
    """Capture request body within `snoop` so we can inspect that the request body is constructed correctly (e.g. for streaming requests).

    See https://github.com/getsentry/responses#dynamic-responses
    """
    snoop["payload"] = list(request.body)
    return status, {}, json.dumps(response_json)


def stringify(updates):
    return [json.dumps(u) for u in updates]
