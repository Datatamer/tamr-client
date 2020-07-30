from functools import wraps
from inspect import getfile
from json import load
from pathlib import Path

import responses

tests_tc_dir = (Path(__file__) / "..").resolve()
fake_json_dir = tests_tc_dir / "fake_json"


def _to_kwargs(fake):
    req = fake["request"]
    resp = fake["response"]
    return {**req, **resp}


def json(test_fn):
    test_file = Path(getfile(test_fn))

    fakes_mod_path = fake_json_dir / test_file.relative_to(tests_tc_dir).with_suffix("")
    fakes_test_path = (fakes_mod_path / test_fn.__name__).with_suffix(".json")
    with open(fakes_test_path) as f:
        fakes = load(f)

    @wraps(test_fn)
    def wrapper(*args, **kwargs):
        with responses.RequestsMock() as rsps:
            for fake in fakes:
                rsps.add(**_to_kwargs(fake))
            test_fn(*args, **kwargs)

    return wrapper
