from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Instance:
    protocol: str = "http"
    host: str = "localhost"
    port: Optional[int] = None


def origin(instance: Instance) -> str:
    """HTTP origin i.e. :code:`<protocol>://<host>[:<port>]`.

    For additional information, see `MDN web docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_ .
    """
    if instance.port is None:
        return f"{instance.protocol}://{instance.host}"
    else:
        return f"{instance.protocol}://{instance.host}:{instance.port}"
