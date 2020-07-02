from dataclasses import dataclass
from typing import Optional, Union

from tamr_client._types.url import URL


@dataclass(frozen=True)
class MasteringProject:
    """A Tamr Mastering project

    See https://docs.tamr.com/reference/the-project-object

    Args:
        url
        name
        description
    """

    url: URL
    name: str
    description: Optional[str] = None


Project = Union[MasteringProject]
