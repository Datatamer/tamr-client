from dataclasses import dataclass

from tamr_client.instance import Instance
import tamr_client.instance as instance

@dataclass(frozen=True)
class URL:
    path: str
    instance: Instance = Instance()
    base_path: str = "api/versioned/v1"

    def __str__(self):
        origin = instance.origin(self.instance)
        return f"{origin}/{self.base_path}/{self.path}"
