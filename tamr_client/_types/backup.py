from dataclasses import dataclass

from tamr_client._types.url import URL


@dataclass(frozen=True)
class Backup:
    """A Tamr backup

    See https://docs.tamr.com/new/docs/configuration-backup-and-restore

    Args:
        url
        path
        state
        error_message
    """

    url: URL
    path: str
    state: str
    error_message: str
