"""
See https://docs.tamr.com/reference/dataset-models
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple
from tamr_client import response
from tamr_client.instance import Instance
from tamr_client.session import Session
from tamr_client.types import JsonDict
from tamr_client.url import URL
@dataclass(frozen=True)
class UnifiedDataset:
    """A Tamr dataset

    See https://docs.tamr.com/reference/dataset-models

    Args:
        url
        key_attribute_names
    """

    url: URL
    name: str
    key_attribute_names: Tuple[str, ...]
    description: Optional[str] = None

def commit(unified_dataset: UnifiedDataset, session: Session, instance: Instance) -> JsonDict:
