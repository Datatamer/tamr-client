from dataclasses import dataclass
from typing import Optional, Union

from tamr_client._types.attribute import Attribute
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


@dataclass(frozen=True)
class UnknownProject:
    """A Tamr project of an unrecognized type

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
    CategorizationProject,
    MasteringProject,
    SchemaMappingProject,
    GoldenRecordsProject,
    UnknownProject,
]


@dataclass(frozen=True)
class AttributeMapping:
    """A Tamr Attribute Mapping.

    See https://docs.tamr.com/new/reference/retrieve-projects-mappings

    Args:
        url
        input_attribute
        unified_attribute
    """

    url: URL
    input_attribute: Attribute
    unified_attribute: Attribute
