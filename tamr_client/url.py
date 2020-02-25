from dataclasses import dataclass

import tamr_client as tc


@dataclass(frozen=True)
class URL:
    path: str
    instance: tc.Instance = tc.Instance()
    base_path: str = "api/versioned/v1"

    def __str__(self):
        origin = tc.instance.origin(self.instance)
        return f"{origin}/{self.base_path}/{self.path}"
