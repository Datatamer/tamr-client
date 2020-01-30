# flake8: noqa

import logging

from tamr_unify_client.client import Client

# utilities
from tamr_unify_client.url import URL
import tamr_unify_client.response as response
import tamr_unify_client.url as url

# attributes
from tamr_unify_client.attributes.attribute_type import AttributeType
import tamr_unify_client.attributes.attribute_type as attribute_type
from tamr_unify_client.attributes.subattribute import SubAttribute
import tamr_unify_client.attributes.subattribute as subattribute
from tamr_unify_client.attributes.attribute import Attribute
import tamr_unify_client.attributes.attribute as attribute

# datasets
import tamr_unify_client.datasets.dataset as dataset

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())
