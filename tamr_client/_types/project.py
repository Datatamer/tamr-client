from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

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


SimilarityFunction = Enum(
    "SimilarityFunction",
    [
        "COSINE",
        "JACCARD",
        "ABSOLUTE_DIFF",
        "RELATIVE_DIFF",
        "GEOSPATIAL_HAUSDORFF",
        "GEOSPATIAL_DIRECTIONAL_HAUSDORFF",
        "GEOSPATIAL_MIN_DISTANCE",
        "GEOSPATIAL_RELATIVE_HAUSDORFF",
        "GEOSPATIAL_RELATIVE_AREA_OVERLAP",
    ],
)

Tokenizer = Enum(
    "Tokenizer",
    {
        "DEFAULT": "DEFAULT",
        "STEMMING_EN": "STEMMING_EN",
        "REGEX": "REGEX",
        "BIGRAM": "BIGRAM",
        "TRIGRAM": "TRIGRAM",
        "BIWORD": "BIWORD",
        "NONE": "",
    },
)

AttributeRole = Enum(
    "AttributeRole",
    {
        "CLUSTER_NAME_ATTRIBUTE": "CLUSTER_NAME_ATTRIBUTE",
        "SUM_ATTRIBUTE": "SUM_ATTRIBUTE",
        "NONE": "",
    },
)


@dataclass(frozen=True)
class AttributeConfiguration:
    """A Tamr Attribute Configuration.

    See https://docs.tamr.com/previous/reference/attribute-configuration

    Args:
        url
        attribute
        attribute_role
        similarity_function
        enabled_for_ml
        tokenizer
        numeric_field_resolution
    """

    url: URL
    attribute: Attribute
    attribute_role: AttributeRole
    similarity_function: SimilarityFunction
    enabled_for_ml: bool
    tokenizer: Tokenizer
    numeric_field_resolution: List[int]
