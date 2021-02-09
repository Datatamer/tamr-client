"""
See https://docs.tamr.com/new/reference/retrieve-projects-mappings
"""
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from tamr_client import attribute, dataset, response
from tamr_client import project as tc_project
from tamr_client._types import (
    Attribute,
    AttributeMapping,
    Instance,
    JsonDict,
    Project,
    Session,
    URL,
)
from tamr_client.exception import TamrClientException


class NotFound(TamrClientException):
    """Raised when referencing an attribute mapping that does not exist on the server."""

    pass


class AlreadyExists(TamrClientException):
    """Raised when an attribute mapping with these specifications already exists."""

    pass


class Ambiguous(TamrClientException):
    """Raised when an attribute mapping specification is incomplete, ambiguous, or contradictory."""

    pass


def create(
    session: Session,
    project: Project,
    input_attribute: Attribute,
    unified_attribute: Attribute,
) -> AttributeMapping:
    """Create a mapping in Tamr between input attributes and unified attributes of the given project.

    Args:
        project: Tamr project
        input_attribute: The attribute of a source dataset to map
        unified_attribute: The attribute of the unified dataset to map onto

    Returns:
        Attribute mapping created in Tamr

    Raises:
        attribute_mapping.AlreadyExists: If an attribute mapping with these specifications already exists.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    data = {
        "relativeInputAttributeId": input_attribute.url.path,
        "relativeUnifiedAttributeId": unified_attribute.url.path,
    }
    r = session.post(url=str(project.url) + "/attributeMappings", json=data)

    if r.status_code == 204:
        raise AlreadyExists(
            "An attribute mapping with these specifications already exists."
        )
    if r.status_code == 400:
        raise Ambiguous(r.json()["message"])
    if r.status_code == 404:
        if "dataset" in r.json()["message"].lower():
            raise dataset.NotFound(r.json()["message"])
        elif "project" in r.json()["message"].lower():
            raise tc_project.NotFound(r.json()["message"])

    data = response.successful(r).json()
    instance = project.url.instance
    url = URL(instance=instance, path=data["relativeId"])
    return AttributeMapping(
        url,
        input_attribute=attribute._attribute._by_url(
            session, URL(instance=instance, path=data["relativeInputAttributeId"]),
        ),
        unified_attribute=attribute._attribute._by_url(
            session, URL(instance=instance, path=data["relativeUnifiedAttributeId"]),
        ),
    )


def get_all(session: Session, tamr_project: Project) -> List[AttributeMapping]:
    """Get all attribute mappings of a Tamr project

    Args:
        tamr_project: Tamr project

    Returns:
        The attribute mappings of the project

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    url = str(tamr_project.url) + "/attributeMappings"
    r = session.get(url=url)

    data = response.successful(r).json()
    mapping_list = []
    attribute_memo: Dict[URL, Attribute] = {}
    for mapping_data in data:
        mapping, attribute_memo = _get(
            session,
            tamr_project.url.instance,
            mapping_data,
            attribute_memo=attribute_memo,
        )
        mapping_list.append(mapping)
    return mapping_list


def _get(
    session: Session,
    instance: Instance,
    data: JsonDict,
    *,
    attribute_memo: Optional[Dict[URL, Attribute]] = None
) -> Tuple[AttributeMapping, Dict[URL, Attribute]]:
    """Construct an attribute mapping from server response

    This is a utility function used by `attribute_mapping.get_all`. When an attribute is
    fetched, all other attributes in its dataset are also retrieved and stored in a
    dictionary to limit the number of requests made to the server

    Args:
        instance: A Tamr instance
        data: The JSON body of the server response retrieve a project's attribute mappings
        attribute_memo: Dictionary of fetched attributes used to avoid redundant requests

    Returns:
        The attribute mapping and updated memo
    """
    if attribute_memo is None:
        attribute_memo = {}
    cp = deepcopy(data)
    input_attribute_url = URL(instance=instance, path=cp["relativeInputAttributeId"])
    unified_attribute_url = URL(
        instance=instance, path=cp["relativeUnifiedAttributeId"]
    )

    if input_attribute_url not in attribute_memo:
        attr_dataset = dataset.by_resource_id(
            session, instance, cp["relativeInputAttributeId"].split("/")[1]
        )
        attribute_memo = {
            **attribute_memo,
            **{attr.url: attr for attr in dataset.attributes(session, attr_dataset)},
        }
    if unified_attribute_url not in attribute_memo:
        attr_dataset = dataset.by_resource_id(
            session, instance, cp["relativeUnifiedAttributeId"].split("/")[1]
        )
        attribute_memo = {
            **attribute_memo,
            **{attr.url: attr for attr in dataset.attributes(session, attr_dataset)},
        }

    return (
        AttributeMapping(
            url=URL(instance=instance, path=cp["relativeId"]),
            input_attribute=attribute_memo[input_attribute_url],
            unified_attribute=attribute_memo[unified_attribute_url],
        ),
        attribute_memo,
    )


def delete(session: Session, attribute_mapping: AttributeMapping):
    """Delete an existing attribute mapping

    Args:
        attribute_mapping: Existing attribute mapping to delete

    Raises:
        attribute_mapping.NotFound: If no attribute mapping could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.delete(str(attribute_mapping.url))
    if r.status_code == 404:
        raise NotFound(str(attribute_mapping.url))
    response.successful(r)
