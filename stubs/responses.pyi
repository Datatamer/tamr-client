from functools import partial
from typing import Any, Callable, ContextManager, Dict, Optional

JsonDict = Dict[str, Any]

DELETE: str
GET: str
POST: str
PUT: str

def add(
    method: Optional[str] = None,
    url: Optional[str] = None,
    body: Optional[str] = None,
    status: Optional[int] = None,
    json: Optional[JsonDict] = None,
): ...
def activate(Callable) -> Callable: ...
def add_callback(method: Optional[str], url: Optional[str], callback: partial[Any]): ...
def RequestsMock() -> ContextManager[Any]: ...
