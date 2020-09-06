"""
This module includes:
- SubAttribute
- AttributeType
- Attribute

The definition order is chosen to minimize the number of forward references.
See https://www.python.org/dev/peps/pep-0484/#forward-references

Forward references are necessary because
- `SubAttribute` and `AttributeType` recursively depend on each other
- `Array` and `Map` have `AttributeType` fields but are themselves `AttributeType`s
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional, Tuple, Union

from tamr_client._types.url import URL


# sub attribute
###############


@dataclass(frozen=True)
class SubAttribute:
    """An attribute which is itself a property of another attribute.

    See https://docs.tamr.com/reference#attribute-types

    NOTE:
        `sphinx_autodoc_typehints` cannot handle forward reference to `AttributeType`,
        so reference docs are written manually for this type

    Args:
        name: Name of sub-attribute
        type: See https://docs.tamr.com/reference#attribute-types
        is_nullable: If this sub-attribute can be null
    """

    name: str
    type: "AttributeType"
    is_nullable: bool


# attribute types
#################

# primitive types

PrimitiveType = Enum("PrimitiveType", ["BOOLEAN", "DOUBLE", "INT", "LONG", "STRING"])

# primitive type aliases
DOUBLE = PrimitiveType.DOUBLE
BOOLEAN = PrimitiveType.BOOLEAN
INT = PrimitiveType.INT
LONG = PrimitiveType.LONG
STRING = PrimitiveType.STRING

# complex types


@dataclass(frozen=True)
class Array:
    """See https://docs.tamr.com/reference#attribute-types

    NOTE:
        `sphinx_autodoc_typehints` cannot handle forward reference to `AttributeType`,
        so reference docs are written manually for this type

    Args:
        inner_type
    """

    _tag: ClassVar[str] = "ARRAY"
    inner_type: "AttributeType"


@dataclass(frozen=True)
class Map:
    """See https://docs.tamr.com/reference#attribute-types

    NOTE:
        `sphinx_autodoc_typehints` cannot handle forward reference to `AttributeType`,
        so reference docs are written manually for this type

    Args:
        inner_type
    """

    _tag: ClassVar[str] = "MAP"
    inner_type: "AttributeType"


@dataclass(frozen=True)
class Record:
    """See https://docs.tamr.com/reference#attribute-types

    Args:
        attributes
    """

    _tag: ClassVar[str] = "RECORD"
    attributes: Tuple[SubAttribute, ...]


ComplexType = Union[Array, Map, Record]


AttributeType = Union[PrimitiveType, ComplexType]

# complex type aliases
DEFAULT: AttributeType = Array(STRING)
GEOSPATIAL: AttributeType = Record(
    attributes=(
        SubAttribute(name="point", is_nullable=True, type=Array(DOUBLE)),
        SubAttribute(name="multiPoint", is_nullable=True, type=Array(Array(DOUBLE))),
        SubAttribute(name="lineString", is_nullable=True, type=Array(Array(DOUBLE))),
        SubAttribute(
            name="multiLineString", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        SubAttribute(
            name="polygon", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        SubAttribute(
            name="multiPolygon",
            is_nullable=True,
            type=Array(Array(Array(Array(DOUBLE)))),
        ),
    )
)

# attribute
###########


@dataclass(frozen=True)
class Attribute:
    """A Tamr Attribute.

    See https://docs.tamr.com/reference#attribute-types

    Args:
        url
        name
        type
        is_nullable
        description
    """

    url: URL
    name: str
    type: AttributeType
    is_nullable: bool
    description: Optional[str] = None
