# Logging
#########

import logging

# https://docs.python-guide.org/writing/logging/#logging-in-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())

# BETA check
############

from tamr_client import _beta

_beta.check()

# types
#######

from tamr_client._types import (
    AnyDataset,
    Attribute,
    AttributeType,
    Dataset,
    Instance,
    MasteringProject,
    Operation,
    Project,
    Session,
    SubAttribute,
    UnifiedDataset,
    URL,
    UsernamePasswordAuth,
)

# functionality
###############

from tamr_client import attribute
from tamr_client import dataset
from tamr_client import instance
from tamr_client import mastering
from tamr_client import operation
from tamr_client import primary_key
from tamr_client import project
from tamr_client import response
from tamr_client import session
from tamr_client.dataset import dataframe
from tamr_client.dataset import record
from tamr_client.exception import TamrClientException
