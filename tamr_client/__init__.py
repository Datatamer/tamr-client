# flake8: noqa

# BETA check
############

import tamr_client.beta as beta

beta._check()

# Logging
#########

import logging

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Import shortcuts
##################

# utilities
from tamr_client import response

# instance
from tamr_client.instance import Instance
from tamr_client import instance

# url
from tamr_client.url import URL
from tamr_client import url

# auth
from tamr_client.auth import UsernamePasswordAuth

# session
from tamr_client.session import Session
from tamr_client import session

# datasets
from tamr_client.dataset import Dataset, DatasetNotFound
from tamr_client import dataset

# records
from tamr_client.dataset.record import PrimaryKeyNotFound
from tamr_client.dataset import record

# dataframe
from tamr_client.dataset.dataframe import AmbiguousPrimaryKey
from tamr_client.dataset import dataframe

# attributes
from tamr_client.attributes.subattribute import SubAttribute
from tamr_client.attributes import subattribute

from tamr_client.attributes.attribute_type import AttributeType
from tamr_client.attributes import attribute_type

import tamr_client.attributes.type_alias

from tamr_client.attributes.attribute import (
    Attribute,
    ReservedAttributeName,
    AttributeExists,
    AttributeNotFound,
)
from tamr_client.attributes import attribute

from tamr_client import mastering
from tamr_client import project
