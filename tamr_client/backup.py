from copy import deepcopy
from typing import List

from tamr_client import Backup, response
from tamr_client._types import Instance, JsonDict, Session, URL
from tamr_client.exception import TamrClientException


class InvalidOperation(TamrClientException):
    """Raised when attempting an invalid operation.
    """

    pass


class NotFound(TamrClientException):
    """Raised when referencing a backup that does not exist on the server.
    """

    pass


def _from_json(url: URL, data: JsonDict) -> Backup:
    """Make backup from JSON data (deserialize).

    Args:
        url: Backup URL
        data: Backup JSON data from Tamr server
    """
    cp = deepcopy(data)
    return Backup(
        url=url,
        path=cp["backupPath"],
        state=cp["state"],
        error_message=cp["errorMessage"],
    )


def get_all(session: Session, instance: Instance) -> List[Backup]:
    """Get all backups that have been initiated for a Tamr instance.

    Args:
        session: Tamr session
        instance: Tamr instance

    Returns:
        A list of Tamr backups

    Raises:
        backup.NotFound: If no backup found at the specified URL
    """
    url = URL(instance=instance, path="backups")
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    backups = [
        _from_json(URL(instance=instance, path=f'backups/{data["relativeId"]}'), data)
        for data in response.successful(r).json()
    ]
    return backups


def by_resource_id(session: Session, instance: Instance, resource_id: str) -> Backup:
    """Get information on a specific Tamr backup.

    Args:
        session: Tamr session
        instance: Tamr instance
        resource_id: Resource ID of the backup

    Returns:
        A Tamr backup

    Raises:
        backup.NotFound: If no backup found at the specified URL
    """
    url = URL(instance=instance, path=f"backups/{resource_id}")
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    return _from_json(url, response.successful(r).json())


def initiate(session: Session, instance: Instance) -> Backup:
    """Initiate a Tamr backup.

    Args:
        session: Tamr session
        instance: Tamr instance

    Returns:
        Initiated backup

    Raises:
        backup.InvalidOperation: If attempting an invalid operation
    """
    url = URL(instance=instance, path="backups")
    r = session.post(str(url))
    if r.status_code == 400:
        raise InvalidOperation(str(url), r.json()["message"])
    data = response.successful(r).json()
    return _from_json(
        URL(instance=instance, path=f'backups/{data["relativeId"]}'), data
    )


def cancel(session: Session, backup: Backup) -> Backup:
    """Cancel a Tamr backup.

    Args:
        session: Tamr session
        backup: A Tamr backup

    Returns:
        Canceled backup

    Raises:
        backup.NotFound: If no backup found at the specified URL
        backup.InvalidOperation: If attempting an invalid operation
    """
    cancel_url = f"{backup.url}:cancel"
    r = session.post(cancel_url)
    if r.status_code == 404:
        raise NotFound(cancel_url)
    if r.status_code == 400:
        raise InvalidOperation(cancel_url, r.json()["message"])
    return _from_json(backup.url, response.successful(r).json())


def poll(session: Session, backup: Backup) -> Backup:
    """Poll this backup for server-side updates.

    Does not update the :class:`~tamr_client.backup.Backup` object.
    Instead, returns a new :class:`~tamr_client.backup.Backup`.

    Args:
        session: Tamr session
        backup: Tamr backup to be polled

    Returns:
        A Tamr backup

    Raises:
        backup.NotFound: If no backup found at the specified URL
    """
    url = backup.url
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    return _from_json(url, response.successful(r).json())
