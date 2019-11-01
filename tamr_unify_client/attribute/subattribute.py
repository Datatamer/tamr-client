from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from tamr_unify_client.attribute.type import AttributeType

SubAttributeJson = Dict[str, Any]


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
    type: AttributeType
    is_nullable: bool
    _json: SubAttributeJson = field(repr=False)
    description: Optional[str] = None

    @staticmethod
    def from_json(data: SubAttributeJson) -> "SubAttribute":
        """Create a SubAttribute from JSON data.

        Args:
            data: JSON data received from Tamr server.
        """
        _json = deepcopy(data)

        dc = deepcopy(data)
        dc["is_nullable"] = dc.pop("isNullable")

        type_json = dc.pop("type")
        # TODO implement AttributeType.from_json and use that instead
        type = AttributeType(type_json)

        return SubAttribute(**dc, type=type, _json=_json)
