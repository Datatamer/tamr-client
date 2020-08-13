"""
See https://docs.tamr.com/reference#attribute-types
"""
import logging

from tamr_client._types import (
    Array,
    AttributeType,
    JsonDict,
    Map,
    PrimitiveType,
    Record,
)
from tamr_client._types import (  # noqa: F401
    BOOLEAN,
    DEFAULT,
    DOUBLE,
    GEOSPATIAL,
    INT,
    LONG,
    STRING,
)
from tamr_client.attribute import sub

logger = logging.getLogger(__name__)


def from_json(data: JsonDict) -> AttributeType:
    """Make an attribute type from JSON data (deserialize)

    Args:
        data: JSON data from Tamr server
    """
    base_type = data.get("baseType")
    if base_type is None:
        logger.error(f"JSON data: {repr(data)}")
        raise ValueError("Missing required field 'baseType'.")

    for primitive in PrimitiveType:
        if base_type == primitive.name:
            return primitive

    if base_type == Array._tag:
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
        return Record(attributes=tuple([sub.from_json(attr) for attr in attributes]))
    else:
        logger.error(f"JSON data: {repr(data)}")
        raise ValueError(f"Unrecognized 'baseType': {base_type}")


def to_json(attr_type: AttributeType) -> JsonDict:
    """Serialize attribute type to JSON

    Args:
        attr_type: Attribute type to serialize
    """
    if isinstance(attr_type, PrimitiveType):
        return {"baseType": attr_type.name}
    elif isinstance(attr_type, (Array, Map)):
        return {
            "baseType": type(attr_type)._tag,
            "innerType": to_json(attr_type.inner_type),
        }
    elif isinstance(attr_type, Record):

        return {
            "baseType": type(attr_type)._tag,
            "attributes": [sub.to_json(attr) for attr in attr_type.attributes],
        }
    else:
        raise TypeError(attr_type)
