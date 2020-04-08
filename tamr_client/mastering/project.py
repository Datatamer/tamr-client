from dataclasses import dataclass
from typing import Optional

import tamr_client as tc
from tamr_client.types import JsonDict


@dataclass(frozen=True)
class Project:
    """A Tamr Mastering project

    See https://docs.tamr.com/reference/the-project-object

    Args:
        url
        name
        description
    """

    url: tc.URL
    name: str
    description: Optional[str] = None


def _from_json(url: tc.URL, data: JsonDict) -> Project:
    """Make mastering project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    return tc.mastering.Project(
        url, name=data["name"], description=data.get("description")
    )
