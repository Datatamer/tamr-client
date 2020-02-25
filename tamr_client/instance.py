from dataclasses import dataclass


@dataclass(frozen=True)
class Instance:
    protocol: str = "http"
    host: str = "localhost"
    port: int = 9100


def origin(instance: Instance) -> str:
    """HTTP origin i.e. :code:`<protocol>://<host>[:<port>]`.

    For additional information, see `MDN web docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_ .
    """
    return f"{instance.protocol}://{instance.host}:{instance.port}"
