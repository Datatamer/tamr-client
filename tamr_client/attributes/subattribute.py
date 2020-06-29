"""This module and attribute_type depend on each other.

"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from tamr_client._types import JsonDict

if TYPE_CHECKING:
    from tamr_client.attributes.attribute_type import AttributeType


@dataclass(frozen=True)
class SubAttribute:
    """An attribute which is itself a property of another attribute.

    See https://docs.tamr.com/reference#attribute-types

    Args:
        name: Name of sub-attribute
        description: Description of sub-attribute
        type: See https://docs.tamr.com/reference#attribute-types
        is_nullable: If this sub-attribute can be null
    """

    name: str
    type: "AttributeType"
    is_nullable: bool
    description: Optional[str] = None


def from_json(data: JsonDict) -> SubAttribute:
    """Make a SubAttribute from JSON data (deserialize)

    Args:
        data: JSON data received from Tamr server.
    """
    from tamr_client.attributes import attribute_type

    cp = deepcopy(data)
    d = {}
    d["name"] = cp["name"]
    d["is_nullable"] = cp["isNullable"]
    d["type"] = attribute_type.from_json(cp["type"])
    return SubAttribute(**d)


def to_json(subattr: SubAttribute) -> JsonDict:
    """Serialize subattribute into JSON

    Args:
        subattr: SubAttribute to serialize
    """
    from tamr_client.attributes import attribute_type

    d = {
        "name": subattr.name,
        "type": attribute_type.to_json(subattr.type),
        "isNullable": subattr.is_nullable,
    }
    if subattr.description is not None:
        d["description"] = subattr.description
    return d
