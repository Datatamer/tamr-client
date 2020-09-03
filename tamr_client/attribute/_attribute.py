"""
See https://docs.tamr.com/reference/attribute-types
"""
from copy import deepcopy
from dataclasses import replace
from typing import Optional

from tamr_client import response
from tamr_client._types import Attribute, AttributeType, Dataset, JsonDict, Session, URL
from tamr_client.attribute import type as attribute_type
from tamr_client.exception import TamrClientException


_RESERVED_NAMES = frozenset(
    [
        # See javasrc/procurify/ui/app/scripts/constants/ElasticConstants.js
        "origin_source_name",
        "tamr_id",
        "origin_entity_id",
        # See javasrc/procurify/ui/app/scripts/constants/PipelineConstants.js
        "clusterId",
        "originSourceId",
        "originEntityId",
        "sourceId",
        "entityId",
        "suggestedClusterId",
        "verificationType",
        "verifiedClusterId",
    ]
)


class AlreadyExists(TamrClientException):
    """Raised when trying to create an attribute that already exists on the server"""

    pass


class NotFound(TamrClientException):
    """Raised when referencing (e.g. updating or deleting) an attribute
    that does not exist on the server.
    """

    pass


class ReservedName(TamrClientException):
    """Raised when attempting to create an attribute with a reserved name"""

    pass


def by_resource_id(session: Session, dataset: Dataset, id: str) -> Attribute:
    """Get attribute by resource ID

    Fetches attribute from Tamr server

    Args:
        dataset: Dataset containing this attribute
        id: Attribute ID

    Raises:
        attribute.NotFound: If no attribute could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = replace(dataset.url, path=dataset.url.path + f"/attributes/{id}")
    return _by_url(session, url)


def _by_url(session: Session, url: URL) -> Attribute:
    """Get attribute by URL

    Fetches attribute from Tamr server

    Args:
        url: Attribute URL

    Raises:
        attribute.NotFound: If no attribute could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> Attribute:
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
        type=attribute_type.from_json(cp["type"]),
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
        "type": attribute_type.to_json(attr.type),
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
    is_nullable: bool,
    type: AttributeType = attribute_type.DEFAULT,
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
        force: If `True`, skips reserved attribute name check

    Returns:
        The newly created attribute

    Raises:
        attribute.ReservedName: If attribute name is reserved.
        attribute.AlreadyExists: If an attribute already exists at the specified URL.
            Corresponds to a 409 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    if name in _RESERVED_NAMES:
        raise ReservedName(name)

    return _create(
        session,
        dataset,
        name=name,
        is_nullable=is_nullable,
        type=type,
        description=description,
    )


def _create(
    session: Session,
    dataset: Dataset,
    *,
    name: str,
    is_nullable: bool,
    type: AttributeType = attribute_type.DEFAULT,
    description: Optional[str] = None,
) -> Attribute:
    """Same as `tc.attribute.create`, but does not check for reserved attribute
    names.
    """
    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    url = replace(attrs_url, path=attrs_url.path + f"/{name}")

    body = {
        "name": name,
        "type": attribute_type.to_json(type),
        "isNullable": is_nullable,
    }
    if description is not None:
        body["description"] = description

    r = session.post(str(attrs_url), json=body)
    if r.status_code == 409:
        raise AlreadyExists(str(url))
    data = response.successful(r).json()

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
        attribute.NotFound: If no attribute could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    updates = {"description": description}
    r = session.put(str(attribute.url), json=updates)
    if r.status_code == 404:
        raise NotFound(str(attribute.url))
    data = response.successful(r).json()
    return _from_json(attribute.url, data)


def delete(session: Session, attribute: Attribute):
    """Deletes an existing attribute

    Sends a deletion request to the Tamr server

    Args:
        attribute: Existing attribute to delete

    Raises:
        attribute.NotFound: If no attribute could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.delete(str(attribute.url))
    if r.status_code == 404:
        raise NotFound(str(attribute.url))
    response.successful(r)
