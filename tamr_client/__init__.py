# flake8: noqa

############
# BETA start
############

import os
import sys

beta_flag_name = "TAMR_CLIENT_BETA"
beta_flag_value = "1"
beta_flag = os.environ.get(beta_flag_name)

if beta_flag != beta_flag_value:
    msg = (
        f"'tamr_client' package is in BETA, but you do not have the '{beta_flag_name}' environment variable set to '1'."
        f"\nSet '{beta_flag_name}=1' to opt-in to BETA features."
        "\n\nWARNING: Do not rely on BETA features in production workflows."
        "\nTamr will not offer support for BETA features."
    )
    print(msg)
    sys.exit(1)

##########
# BETA end
##########

import logging

# utilities
import tamr_client.response as response

# instance
from tamr_client.instance import Instance
import tamr_client.instance as instance

# url
from tamr_client.url import URL
import tamr_client.url as url

# auth
from tamr_client.auth import UsernamePasswordAuth

# session
from tamr_client.session import Session
import tamr_client.session as session

# datasets
from tamr_client.datasets.dataset import Dataset, DatasetNotFound
import tamr_client.datasets.dataset as dataset

# attributes
from tamr_client.attributes.subattribute import SubAttribute
import tamr_client.attributes.subattribute as subattribute

from tamr_client.attributes.attribute_type import AttributeType
import tamr_client.attributes.attribute_type as attribute_type

import tamr_client.attributes.type_alias

from tamr_client.attributes.attribute import (
    Attribute,
    ReservedAttributeName,
    AttributeExists,
    AttributeNotFound,
)
import tamr_client.attributes.attribute as attribute

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())
