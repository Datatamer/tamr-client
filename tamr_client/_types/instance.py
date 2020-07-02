from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Instance:
    """Connection parameters for a running Tamr instance

    Args:
        protocol
        host
        port
    """

    protocol: str = "http"
    host: str = "localhost"
    port: Optional[int] = None
