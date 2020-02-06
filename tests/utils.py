import json
from pathlib import Path
from typing import Union

import tamr_client as tc

data_dir = Path(__file__).parent / "data"


def load_json(path: Union[str, Path]):
    with open(data_dir / path) as f:
        return json.load(f)


def session():
    auth = tc.UsernamePasswordAuth("admin", "dt")
    s = tc.session(auth)
    return s


def dataset():
    url = tc.URL(path="datasets/1")
    dataset = tc.Dataset(url, key_attribute_names=("primary_key",))
    return dataset
