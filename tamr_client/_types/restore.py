from dataclasses import dataclass

from tamr_client._types.url import URL


@dataclass(frozen=True)
class Restore:
    """A Tamr restore

    See https://docs.tamr.com/new/docs/configuration-backup-and-restore

    Args:
        url
        backup_path
        state
        error_message
    """

    url: URL
    backup_path: str
    state: str
    error_message: str
