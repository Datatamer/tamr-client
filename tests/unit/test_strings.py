from tamr_unify_client import Client
from tamr_unify_client.auth import TokenAuth, UsernamePasswordAuth
from tamr_unify_client.dataset.status import DatasetStatus


def test_client_repr():
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)
    full_clz_name = "tamr_unify_client.client.Client"

    rstr = f"{unify!r}"

    assert rstr.startswith(f"{full_clz_name}(")
    assert "http" in rstr
    assert "password" not in rstr
    assert rstr.endswith(")")

    # further testing when Client has optional arguments
    unify = Client(auth, protocol="http", port=1234, base_path="foo/bar")
    rstr = f"{unify!r}"

    assert "'http'" in rstr
    assert "1234" in rstr
    assert "foo/bar" in rstr


def test_username_auth_repr():
    auth = UsernamePasswordAuth("myusername", "SECRET")
    full_clz_name = "tamr_unify_client.auth.username_password.UsernamePasswordAuth"

    rstr = f"{auth!r}"

    assert rstr.startswith(f"{full_clz_name}(")
    assert "myusername" in rstr
    assert "SECRET" not in rstr
    assert rstr.endswith(")")


def test_token_auth_repr():
    auth = TokenAuth("SECRETTOKEN")
    full_clz_name = "tamr_unify_client.auth.token.TokenAuth"

    rstr = f"{auth!r}"

    assert rstr == f"{full_clz_name}()"
    assert "SECRETTOKEN" not in rstr


def test_dataset_status_repr():
    client = Client(UsernamePasswordAuth("username", "password"))
    data = {
        "relativeId": "path/to/thing/1",
        "datasetName": "testdsname",
        "relativeDatasetId": "path/to/data/1",
        "isStreamable": True,
    }
    status = DatasetStatus.from_json(client, data)
    full_clz_name = "tamr_unify_client.dataset.status.DatasetStatus"

    rstr = f"{status!r}"

    assert rstr.startswith(f"{full_clz_name}(")
    assert "testdsname" in rstr
    assert "True" in rstr
    assert "path/to/thing" in rstr
    assert rstr.endswith(")")


def test_dataset_collection_repr():
    client = Client(UsernamePasswordAuth("username", "password"))
    full_clz_name = "tamr_unify_client.dataset.collection.DatasetCollection"

    rstr = f"{client.datasets!r}"

    assert rstr.startswith(f"{full_clz_name}(")
    assert "api_path='datasets'" in rstr
    assert rstr.endswith(")")
