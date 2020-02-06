# flake8: noqa

import logging

# utilities
from tamr_client.url import URL
import tamr_client.url as url

import tamr_client.response as response
from tamr_client.auth import UsernamePasswordAuth
from tamr_client.session import session

# datasets
from tamr_client.datasets.dataset import Dataset
import tamr_client.datasets.dataset as dataset

# attributes
from tamr_client.attributes.subattribute import SubAttribute
import tamr_client.attributes.subattribute as subattribute

from tamr_client.attributes.attribute_type import AttributeType
import tamr_client.attributes.attribute_type as attribute_type

import tamr_client.attributes.type_alias as attribute_type_alias

from tamr_client.attributes.attribute import Attribute
from tamr_client.attributes.attribute import ReservedAttributeName
from tamr_client.attributes.attribute import AttributeExists
from tamr_client.attributes.attribute import AttributeNotFound
import tamr_client.attributes.attribute as attribute

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())
