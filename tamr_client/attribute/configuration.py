"""
See https://docs.tamr.com/previous/reference/attribute-configuration
"""
from copy import deepcopy
from dataclasses import replace
from typing import List, Optional, Tuple

from tamr_client import attribute, response
from tamr_client._types import (
    Attribute,
    AttributeConfiguration,
    AttributeRole,
    JsonDict,
    Project,
    Session,
    SimilarityFunction,
    Tokenizer,
    URL,
)
from tamr_client.exception import TamrClientException


class AlreadyExists(TamrClientException):
    """Raised when an attribute configuration with these specifications already exists."""

    pass


class NotFound(TamrClientException):
    """Raised when referencing an attribute configuration that does not exist on the server."""

    pass


class Ambiguous(TamrClientException):
    """Raised when an attribute configuration specification is incomplete, ambiguous, or contradictory."""

    pass


class Invalid(TamrClientException):
    """Raised when an improper configuration is specified."""

    pass


def _from_json(
    url: URL, unified_attribute: Attribute, data: JsonDict
) -> AttributeConfiguration:
    """Make attribute configuration from JSON data (deserialize)

    Args:
        url: Attribute configuration URL
        data: Attribute configuration JSON data from Tamr server
    """
    cp = deepcopy(data)
    return AttributeConfiguration(
        url,
        attribute=unified_attribute,
        attribute_role=AttributeRole[cp["attributeRole"]]
        if len(cp["attributeRole"]) > 0
        else AttributeRole.NONE,
        similarity_function=SimilarityFunction[cp["similarityFunction"]],
        enabled_for_ml=cp["enabledForMl"],
        tokenizer=Tokenizer[cp["tokenizer"]]
        if len(cp["tokenizer"]) > 0
        else Tokenizer.NONE,
        numeric_field_resolution=cp["numericFieldResolution"],
    )


def _by_url(session: Session, url: URL) -> AttributeConfiguration:
    """Get attribute configuration by URL

    Fetches attribute configuration from Tamr server

    Args:
        url: Attribute configuration URL

    Raises:
        attribute.configuration.NotFound: If no attribute configuration could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()

    # Construct attribute configuration
    return _with_attribute(session, url, data)


def _with_attribute(
    session: Session, url: URL, data: JsonDict
) -> AttributeConfiguration:
    """Get attribute configuration with relevant attribute constructed

    Fetches attribute configuration from Tamr server

    Args:
        url: Attribute configuration URL
        data: Attribute configuration JSON data from Tamr server

    Raises:
        attribute.NotFound: If no attribute could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    cp = deepcopy(data)
    # Get unified attribute
    attribute_id = "/".join(cp["relativeAttributeId"].split("/")[2:])
    attribute_path = "/".join(cp["relativeId"].split("/")[:2]) + "/" + attribute_id
    attribute_url = replace(url, path=attribute_path)
    unified_attribute = attribute._by_url(session, attribute_url)

    # Construct attribute configuration
    return _from_json(url, unified_attribute, cp)


def by_resource_id(
    session: Session, project: Project, id: str
) -> AttributeConfiguration:
    """Get attribute configuration by resource ID

    Fetches attribute configuration from Tamr server

    Args:
        project: Project containing this attribute configuration
        id: Attribute configuration ID

    Raises:
        attribute.configuration.NotFound: If no attribute configuration could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    url = replace(project.url, path=project.url.path + f"/attributeConfigurations/{id}")
    return _by_url(session, url)


def create(
    session: Session,
    project: Project,
    *,
    unified_attribute: Attribute,
    attribute_role: AttributeRole = AttributeRole.NONE,
    similarity_function: SimilarityFunction = SimilarityFunction.COSINE,
    enabled_for_ml: bool = True,
    tokenizer: Optional[Tokenizer] = None,
    numeric_field_resolution: Optional[List[int]] = None,
) -> AttributeConfiguration:
    """Create an attribute in Tamr for the given project.

    Args:
        project: Tamr project
        unified_attribute: The attribute of the unified dataset to configure
        attribute_role: The role of the attribute as spend or cluster name
        similarity_function: The similarity function to use for this attribute
        enabled_for_ml: Whether to include this attribute in the machine-learning model
        tokenizer: The tokenizer to use for this attribute for text similarity functions
        numeric_field_resolution: Resolution to use for numeric similarity functions

    Returns:
        Attribute configuration created in Tamr

    Raises:
        attribute.configuration.AlreadyExists: If an attribute configuration already exists.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    if numeric_field_resolution is None:
        numeric_field_resolution = []
    if similarity_function in [SimilarityFunction.COSINE, SimilarityFunction.JACCARD]:
        # Use default tokenizer if none passed
        if tokenizer is None:
            tokenizer = Tokenizer.DEFAULT
        elif tokenizer not in Tokenizer or tokenizer == Tokenizer.NONE:
            raise Invalid("A tokenizer must be used with text similarity functions.")
        if len(numeric_field_resolution) > 0:
            raise Invalid(
                "Numeric field resolution cannot be used for text similarity functions."
            )
    else:
        if tokenizer is None:
            tokenizer = Tokenizer.NONE
        if tokenizer != Tokenizer.NONE:
            raise Invalid(
                "A tokenizer cannot be used with non-text similarity functions."
            )

    data = {
        "attributeName": unified_attribute.name,
        "attributeRole": attribute_role.value,
        "similarityFunction": similarity_function.name,
        "enabledForMl": enabled_for_ml,
        "tokenizer": tokenizer.value,
        "numericFieldResolution": numeric_field_resolution,
    }

    r = session.post(url=str(project.url) + "/attributeConfigurations", json=data)

    # Note: This call will create a unified attribute (name only) if it does not already exist
    if r.status_code == 409:
        raise AlreadyExists(
            "An attribute configuration for this attribute already exists."
        )
    if r.status_code == 400:
        raise Ambiguous(r.json()["message"])

    data = response.successful(r).json()
    url = replace(project.url, path=str(data["relativeId"]))
    return _from_json(url, unified_attribute, data)


def update(
    session: Session,
    attribute_configuration: AttributeConfiguration,
    *,
    attribute_role: Optional[AttributeRole] = None,
    similarity_function: Optional[SimilarityFunction] = None,
    enabled_for_ml: Optional[bool] = None,
    tokenizer: Optional[Tokenizer] = None,
    numeric_field_resolution: Optional[List[int]] = None,
) -> AttributeConfiguration:
    """Update an existing attribute configuration in Tamr.

    Args:
        attribute_configuration: Existing attribute configuration to update
        attribute_role: The role of the attribute as spend or cluster name
        similarity_function: The similarity function to use
        enabled_for_ml: Whether to include this attribute in the machine-learning model
        tokenizer: The tokenizer to use for text similarity functions
        numeric_field_resolution: Resolution to use for numeric similarity functions

    Returns:
        Attribute configuration updated in Tamr

    Raises:
        attribute.configuration.NotFound: If no attribute configuration could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    # Use current values as defaults for non-nullable values
    if attribute_role is None:
        attribute_role = attribute_configuration.attribute_role
    if similarity_function is None:
        similarity_function = attribute_configuration.similarity_function
    if enabled_for_ml is None:
        enabled_for_ml = attribute_configuration.enabled_for_ml

    # Null numeric field resolution if similarity function is text
    # Null default tokenizer if similarity function is non-text
    if similarity_function in [SimilarityFunction.COSINE, SimilarityFunction.JACCARD]:
        if numeric_field_resolution is None:
            numeric_field_resolution = []
        if tokenizer is None:
            tokenizer = attribute_configuration.tokenizer
        if tokenizer not in Tokenizer or tokenizer == Tokenizer.NONE:
            raise Invalid("A tokenizer must be used with text similarity functions.")
        if len(numeric_field_resolution) > 0:
            raise Invalid(
                "Numeric field resolution cannot be used for text similarity functions."
            )
    else:
        if numeric_field_resolution is None:
            numeric_field_resolution = attribute_configuration.numeric_field_resolution
        if tokenizer is None:
            tokenizer = Tokenizer.NONE
        if tokenizer != Tokenizer.NONE:
            raise Invalid(
                "A tokenizer cannot be used with non-text similarity functions."
            )

    data = {
        "attributeName": attribute_configuration.attribute.name,
        "attributeRole": attribute_role.value,
        "similarityFunction": similarity_function.name,
        "enabledForMl": enabled_for_ml,
        "tokenizer": tokenizer.value,
        "numericFieldResolution": numeric_field_resolution,
    }

    r = session.put(url=str(attribute_configuration.url), json=data)

    if r.status_code == 404:
        raise NotFound(str(attribute_configuration.url))
    if r.status_code == 400:
        raise Ambiguous(r.json()["message"])

    return _from_json(
        attribute_configuration.url,
        unified_attribute=attribute_configuration.attribute,
        data=data,
    )


def get_all(session: Session, project: Project) -> Tuple[AttributeConfiguration, ...]:
    """Get all attribute configurations of a Tamr project

    Args:
        project: Tamr project

    Returns:
        The attribute configurations of the project

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    url = str(project.url) + "/attributeConfigurations"
    r = session.get(url=url)
    data = response.successful(r).json()
    attr_configs = [
        _with_attribute(session, replace(project.url, path=d["relativeId"]), d)
        for d in data
    ]

    return tuple(attr_configs)


def delete(session: Session, attribute_configuration: AttributeConfiguration):
    """Delete an existing attribute configuration

    Args:
        attribute_configuration: Existing attribute configuration to delete

    Raises:
        attribute.configuration.NotFound: If no attribute mapping could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.delete(str(attribute_configuration.url))
    if r.status_code == 404:
        raise NotFound(str(attribute_configuration.url))
    response.successful(r)
