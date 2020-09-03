"""This module and attribute_type depend on each other.

"""
from copy import deepcopy

from tamr_client._types import JsonDict, SubAttribute
from tamr_client.attribute import type as attribute_type


def from_json(data: JsonDict) -> SubAttribute:
    """Make a SubAttribute from JSON data (deserialize)

    Args:
        data: JSON data received from Tamr server.
    """

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

    d = {
        "name": subattr.name,
        "type": attribute_type.to_json(subattr.type),
        "isNullable": subattr.is_nullable,
    }
    return d
