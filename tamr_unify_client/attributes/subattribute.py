from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import tamr_unify_client as tc
from tamr_unify_client.JsonDict import JsonDict


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
    type: tc.AttributeType
    is_nullable: bool
    description: Optional[str] = None


def from_json(data: JsonDict) -> SubAttribute:
    """Make a SubAttribute from JSON data (deserialize)

    Args:
        data: JSON data received from Tamr server.
    """
    cp = deepcopy(data)
    d = {}
    d["name"] = cp["name"]
    d["is_nullable"] = cp["isNullable"]
    d["type"] = tc.attribute_type.from_json(cp["type"])
    return SubAttribute(**d)


def to_json(subattr: SubAttribute) -> JsonDict:
    """Serialize subattribute into JSON

    Args:
        subattr: SubAttribute to serialize
    """
    d = {
        "name": subattr.name,
        "type": tc.attribute_type.to_json(subattr.type),
        "isNullable": subattr.is_nullable,
    }
    if subattr.description is not None:
        d["description"] = subattr.description
    return d
