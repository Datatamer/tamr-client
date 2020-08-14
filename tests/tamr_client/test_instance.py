import tamr_client as tc
from tests.tamr_client import fake

def test_instance_default():
    instance = tc.Instance()
    assert tc.instance.origin(instance) == "http://localhost"


def test_client_set_protocol():
    instance = tc.Instance(protocol="https")
    assert tc.instance.origin(instance) == "https://localhost"


def test_client_set_host():
    instance = tc.Instance(host="123.123.123.123")
    assert tc.instance.origin(instance) == "http://123.123.123.123"


def test_client_set_port():
    instance = tc.Instance(port=9100)
    assert tc.instance.origin(instance) == "http://localhost:9100"

@fake.json
def test_version():
    s = fake.session()
    instance = fake.instance()
    version = tc.instance.version(s,instance)
    assert version == "2020.012.0"
