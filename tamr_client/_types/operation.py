from dataclasses import dataclass
from typing import Dict, Optional

from tamr_client._types.url import URL


@dataclass(frozen=True)
class Operation:
    """A Tamr operation

    See https://docs.tamr.com/new/reference/the-operation-object

    Args:
        url
        type
        status
        description
    """

    url: URL
    type: str
    status: Optional[Dict[str, str]] = None
    description: Optional[str] = None
