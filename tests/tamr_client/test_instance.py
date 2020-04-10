import tamr_client as tc


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
