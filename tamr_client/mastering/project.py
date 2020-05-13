from dataclasses import dataclass
from typing import Optional

from tamr_client.types import JsonDict
from tamr_client.url import URL


@dataclass(frozen=True)
class Project:
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


def _from_json(url: URL, data: JsonDict) -> Project:
    """Make mastering project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    return Project(url, name=data["name"], description=data.get("description"))
