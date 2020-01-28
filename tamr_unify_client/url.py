from dataclasses import dataclass


@dataclass(frozen=True)
class URL:
    path: str
    protocol: str = "http"
    host: str = "localhost"
    port: int = 9100

    def __str__(self):
        return f"{self.protocol}://{self.host}:{self.port}/{self.path}"
