from typing import Any, Dict, Optional, TypeVar

JsonDict = Dict[str, Any]

DELETE: str
GET: str
POST: str
PUT: str

def add(
    method: Optional[str] = None,
    url: Optional[str] = None,
    status: Optional[int] = None,
    json: Optional[JsonDict] = None,
): ...

T = TypeVar("T")

def activate(T) -> T: ...
