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
    AttributeMapping,
    AttributeType,
    Backup,
    CategorizationProject,
    Dataset,
    GoldenRecordsProject,
    InputTransformation,
    Instance,
    MasteringProject,
    Operation,
    Project,
    Restore,
    SchemaMappingProject,
    Session,
    SubAttribute,
    Transformations,
    UnifiedDataset,
    UnknownProject,
    URL,
    UsernamePasswordAuth,
)

# functionality
###############

from tamr_client import attribute
from tamr_client import backup
from tamr_client import categorization
from tamr_client import dataset
from tamr_client import golden_records
from tamr_client import instance
from tamr_client import mastering
from tamr_client import operation
from tamr_client import primary_key
from tamr_client import project
from tamr_client import response
from tamr_client import restore
from tamr_client import schema_mapping
from tamr_client import session
from tamr_client import transformations
from tamr_client.dataset import dataframe
from tamr_client.dataset import record
from tamr_client.exception import TamrClientException
