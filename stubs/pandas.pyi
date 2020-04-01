from typing import Any, Dict, Iterator, List, Tuple

JsonDict = Dict[str, Any]

class DataFrame:
    columns: Index
    def __init__(self, data: List[JsonDict] = None): ...
    def iterrows(self) -> Iterator[Tuple[int, Series]]: ...

class Series:
    def to_json(self) -> str: ...

class Index:
    def __iter__(self) -> Iterator[str]: ...
