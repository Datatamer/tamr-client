from functools import wraps
from inspect import getfile
from json import load
from pathlib import Path

import responses

import tamr_client as tc


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
    unified_dataset = tc.dataset.unified.UnifiedDataset(
        url, name="dataset.csv", key_attribute_names=("primary_key",)
    )
    return unified_dataset


def mastering_project():
    url = tc.URL(path="projects/1")
    mastering_project = tc.MasteringProject(
        url, name="Project 1", description="A Mastering Project"
    )
    return mastering_project


def transforms():
    return tc.Transformations(
        input_scope=[
            tc.InputTransformation("SELECT *, 1 as one;"),
            tc.InputTransformation("SELECT *, 2 as two;", datasets=[dataset()]),
        ],
        unified_scope=["//Comment\nSELECT *;"],
    )
