from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


def test_client_default():
    auth = UsernamePasswordAuth("username", "password")
    client = Client(auth)

    assert client.origin == "http://localhost:9100"


def test_client_set_protocol():
    auth = UsernamePasswordAuth("username", "password")
    client = Client(auth, protocol="https")

    assert client.origin == "https://localhost:9100"


def test_client_set_host():
    auth = UsernamePasswordAuth("username", "password")
    client = Client(auth, host="123.123.123.123")

    assert client.origin == "http://123.123.123.123:9100"


def test_client_set_port():
    auth = UsernamePasswordAuth("username", "password")
    client = Client(auth, port=80)

    assert client.origin == "http://localhost:80"


def test_client_set_port_none():
    auth = UsernamePasswordAuth("username", "password")
    client = Client(auth, port=None)

    assert client.origin == "http://localhost"
