# BETA check
############

from tamr_client import _beta

_beta.check()

# Logging
#########

import logging

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())

# types
#######

from tamr_client._types import (
    AnyDataset,
    Attribute,
    AttributeType,
    Dataset,
    MasteringProject,
    Project,
    SubAttribute,
    UnifiedDataset,
    URL,
)

# functions
###########

# utilities
from tamr_client import response

# instance
from tamr_client.instance import Instance
from tamr_client import instance

# auth
from tamr_client.auth import UsernamePasswordAuth

# session
from tamr_client.session import Session
from tamr_client import session

# datasets
from tamr_client import dataset

# records
from tamr_client.dataset.record import PrimaryKeyNotFound
from tamr_client.dataset import record

# dataframe
from tamr_client.dataset.dataframe import AmbiguousPrimaryKey
from tamr_client.dataset import dataframe

# attributes
from tamr_client import attribute

from tamr_client import mastering
from tamr_client import project

# operations
from tamr_client.operation import Operation
from tamr_client import operation
