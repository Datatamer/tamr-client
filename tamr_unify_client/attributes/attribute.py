from copy import deepcopy
from dataclasses import dataclass, field, replace
from typing import Optional

from requests import Session

import tamr_unify_client as tc
from tamr_unify_client.dataset.resource import Dataset
from tamr_unify_client.JsonDict import JsonDict


@dataclass(frozen=True)
class Attribute:
    """A Tamr Attribute.

    See https://docs.tamr.com/reference#attribute-types

    Args:
        url
        name
        type
        description
    """

    url: tc.URL
    name: str
    type: tc.attribute_type.AttributeType
    is_nullable: bool
    _json: JsonDict = field(compare=False, repr=False)
    description: Optional[str] = None


def from_resource_id(session: Session, dataset: Dataset, id: str) -> Attribute:
    """Get attribute by resource ID

    Fetches attribute from Tamr server

    Args:
        dataset: Dataset containing this attribute
        id: Attribute ID

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    url = replace(dataset.url, path=dataset.url.path + f"/{id}")
    return _from_url(session, url)


def _from_url(session: Session, url: tc.URL) -> Attribute:
    """Get attribute by URL

    Fetches attribute from Tamr server

    Args:
        url: Attribute URL

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    r = session.get(str(url))
    data = tc.response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: tc.URL, data: JsonDict) -> Attribute:
    """Make attribute from JSON data (deserialize)

    Args:
        url: Attribute URL
        data: Attribute JSON data from Tamr server
    """
    cp = deepcopy(data)
    return Attribute(
        url,
        name=cp["name"],
        description=cp.get("description"),
        is_nullable=cp["isNullable"],
        type=tc.attribute_type.from_json(cp["type"]),
        _json=cp,
    )


def to_json(attr: Attribute) -> JsonDict:
    """Serialize attribute into JSON

    Args:
        attr: Attribute to serialize

    Returns:
        JSON data representing the attribute
    """
    d = {
        "name": attr.name,
        "type": tc.attribute_type.to_json(attr.type),
        "isNullable": attr.is_nullable,
    }
    if attr.description is not None:
        d["description"] = attr.description
    return d


def create(
    session: Session,
    dataset: Dataset,
    *,
    name: str,
    type: tc.attribute_type.AttributeType,
    is_nullable: bool,
    description: Optional[str] = None,
) -> Attribute:
    """Create an attribute

    Posts a creation request to the Tamr server

    Args:
        dataset: Dataset that should contain the new attribute
        name: Name for the new attribute
        type: Attribute type for the new attribute
        is_nullable: Determines if the new attribute can contain NULL values
        description: Description of the new attribute

    Returns:
        The newly created attribute

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")

    body = {
        "name": name,
        "type": tc.attribute_type.to_json(type),
        "isNullable": is_nullable,
    }
    if description is not None:
        body["description"] = description

    r = session.post(str(attrs_url), json=body)
    data = tc.response.successful(r).json()
    name = data["name"]
    url = replace(attrs_url, path=attrs_url.path + f"/{name}")
    return _from_json(url, data)


def update(
    session: Session, attribute: Attribute, *, description: Optional[str] = None
) -> Attribute:
    """Update an existing attribute

    PUTS an update request to the Tamr server

    Args:
        attribute: Existing attribute to update
        description: Updated description for the existing attribute

    Returns:
        The newly updated attribute

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    updates = {"description": description}
    r = session.put(str(attribute.url), json=updates)
    data = tc.response.successful(r).json()
    return _from_json(attribute.url, data)


def delete(session: Session, attribute: Attribute):
    """Deletes an existing attribute

    Sends a deletion request to the Tamr server

    Args:
        attribute: Existing attribute to delete

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    r = session.delete(str(attribute.url))
    tc.response.successful(r)
