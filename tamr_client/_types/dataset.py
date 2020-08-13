from dataclasses import dataclass
from typing import Optional, Tuple, Union

from tamr_client._types.url import URL


@dataclass(frozen=True)
class Dataset:
    """A Tamr dataset

    See https://docs.tamr.com/reference/dataset-models

    Args:
        url: The canonical dataset-based URL for this dataset e.g. `/datasets/1`
        name
        key_attribute_names
        description
    """

    url: URL
    name: str
    key_attribute_names: Tuple[str, ...]
    description: Optional[str] = None


@dataclass(frozen=True)
class UnifiedDataset:
    """A Tamr unified dataset

    See https://docs.tamr.com/reference/dataset-models

    Args:
        url: The project-based alias for this dataset e.g. `/projects/1/unifiedDataset`
        name
        key_attribute_names
        description
    """

    url: URL
    name: str
    key_attribute_names: Tuple[str, ...]
    description: Optional[str] = None


AnyDataset = Union[Dataset, UnifiedDataset]
