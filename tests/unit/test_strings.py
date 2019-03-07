from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


def test_client_repr():
    auth = UsernamePasswordAuth("username", "password")

    unify = Client(auth)
    rstr = f"{unify!r}"

    assert rstr.startswith("tamr_unify_client.client.Client(")
    assert "http" in rstr
    assert rstr.endswith(")")
    assert "password" not in rstr

    unify = Client(auth, protocol="http", port=1234, base_path="foo/bar")
    rstr = f"{unify!r}"

    assert "'http'" in rstr
    assert "1234" in rstr
    assert "foo/bar" in rstr
