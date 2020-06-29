from dataclasses import dataclass

from tamr_client import instance
from tamr_client.instance import Instance


@dataclass(frozen=True)
class URL:
    path: str
    instance: Instance = Instance()
    base_path: str = "api/versioned/v1"

    def __str__(self):
        origin = instance.origin(self.instance)
        return f"{origin}/{self.base_path}/{self.path}"
