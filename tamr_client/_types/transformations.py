from dataclasses import dataclass, field
from typing import List

from tamr_client._types import Dataset


@dataclass(frozen=True)
class InputTransformation:
    transformation: str
    datasets: List[Dataset] = field(default_factory=list)


@dataclass(frozen=True)
class Transformations:
    input_scope: List[InputTransformation] = field(default_factory=list)
    unified_scope: List[str] = field(default_factory=list)
