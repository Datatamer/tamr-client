"""
See https://docs.tamr.com/reference#attribute-types
"""
from dataclasses import dataclass
import logging
from typing import ClassVar, Tuple, Union

import tamr_client as tc
from tamr_client.types import JsonDict

logger = logging.getLogger(__name__)

# primitive types
#################


@dataclass(frozen=True)
class Boolean:
    _tag: ClassVar[str] = "BOOLEAN"


@dataclass(frozen=True)
class Double:
    _tag: ClassVar[str] = "DOUBLE"


@dataclass(frozen=True)
class Int:
    _tag: ClassVar[str] = "INT"


@dataclass(frozen=True)
class Long:
    _tag: ClassVar[str] = "LONG"


@dataclass(frozen=True)
class String:
    _tag: ClassVar[str] = "STRING"


PrimitiveType = Union[Boolean, Double, Int, Long, String]

# complex types
###############


@dataclass(frozen=True)
class Array:
    """See https://docs.tamr.com/reference#attribute-types"""

    # NOTE(pcattori) sphinx_autodoc_typehints cannot handle recursive reference
    # docstring written manually
    _tag: ClassVar[str] = "ARRAY"
    inner_type: "AttributeType"


@dataclass(frozen=True)
class Map:
    """See https://docs.tamr.com/reference#attribute-types"""

    # NOTE(pcattori): sphinx_autodoc_typehints cannot handle recursive reference
    # docstring written manually
    _tag: ClassVar[str] = "MAP"
    inner_type: "AttributeType"


@dataclass(frozen=True)
class Record:
    """See https://docs.tamr.com/reference#attribute-types"""

    # NOTE(pcattori) sphinx_autodoc_typehints cannot handle recursive reference
    # docstring written manually
    _tag: ClassVar[str] = "RECORD"
    attributes: Tuple[tc.SubAttribute, ...]


ComplexType = Union[Array, Map, Record]

# attribute type
################

AttributeType = Union[PrimitiveType, ComplexType]


def from_json(data: JsonDict) -> AttributeType:
    """Make an attribute type from JSON data (deserialize)

    Args:
        data: JSON data from Tamr server
    """
    base_type = data.get("baseType")
    if base_type is None:
        logger.error(f"JSON data: {repr(data)}")
        raise ValueError("Missing required field 'baseType'.")
    if base_type == Boolean._tag:
        return BOOLEAN
    elif base_type == Double._tag:
        return DOUBLE
    elif base_type == Int._tag:
        return INT
    elif base_type == Long._tag:
        return LONG
    elif base_type == String._tag:
        return STRING
    elif base_type == Array._tag:
        inner_type = data.get("innerType")
        if inner_type is None:
            logger.error(f"JSON data: {repr(data)}")
            raise ValueError("Missing required field 'innerType' for Array type.")
        return Array(inner_type=from_json(inner_type))
    elif base_type == Map._tag:
        inner_type = data.get("innerType")
        if inner_type is None:
            logger.error(f"JSON data: {repr(data)}")
            raise ValueError("Missing required field 'innerType' for Map type.")
        return Map(inner_type=from_json(inner_type))
    elif base_type == Record._tag:
        attributes = data.get("attributes")
        if attributes is None:
            logger.error(f"JSON data: {repr(data)}")
            raise ValueError("Missing required field 'attributes' for Record type.")
        return Record(
            attributes=tuple([tc.subattribute.from_json(attr) for attr in attributes])
        )
    else:
        logger.error(f"JSON data: {repr(data)}")
        raise ValueError(f"Unrecognized 'baseType': {base_type}")


def to_json(attr_type: AttributeType) -> JsonDict:
    """Serialize attribute type to JSON

    Args:
        attr_type: Attribute type to serialize
    """
    if isinstance(attr_type, (Boolean, Double, Int, Long, String)):
        return {"baseType": type(attr_type)._tag}
    elif isinstance(attr_type, (Array, Map)):
        return {
            "baseType": type(attr_type)._tag,
            "innerType": to_json(attr_type.inner_type),
        }
    elif isinstance(attr_type, Record):

        return {
            "baseType": type(attr_type)._tag,
            "attributes": [
                tc.subattribute.to_json(attr) for attr in attr_type.attributes
            ],
        }
    else:
        raise TypeError(attr_type)


# Singletons

BOOLEAN = Boolean()
DOUBLE = Double()
INT = Int()
LONG = Long()
STRING = String()
