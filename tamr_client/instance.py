from tamr_client._types import Instance


def origin(instance: Instance) -> str:
    """HTTP origin i.e. :code:`<protocol>://<host>[:<port>]`.

    For additional information, see `MDN web docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_ .
    """
    if instance.port is None:
        return f"{instance.protocol}://{instance.host}"
    else:
        return f"{instance.protocol}://{instance.host}:{instance.port}"
