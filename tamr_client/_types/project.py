from dataclasses import dataclass
from typing import Optional, Union

from tamr_client._types.url import URL


@dataclass(frozen=True)
class CategorizationProject:
    """A Tamr Categorization project

    See https://docs.tamr.com/reference/the-project-object

    Args:
        url
        name
        description
    """

    url: URL
    name: str
    description: Optional[str] = None


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


@dataclass(frozen=True)
class SchemaMappingProject:
    """A Tamr Schema Mapping project

    See https://docs.tamr.com/reference/the-project-object

    Args:
        url
        name
        description
    """

    url: URL
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class GoldenRecordsProject:
    """A Tamr Golden Records project

    See https://docs.tamr.com/reference/the-project-object

    Args:
        url
        name
        description
    """

    url: URL
    name: str
    description: Optional[str] = None


Project = Union[
    CategorizationProject, MasteringProject, SchemaMappingProject, GoldenRecordsProject
]
