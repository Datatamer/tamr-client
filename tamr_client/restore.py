from tamr_client import response, Restore
from tamr_client._types import Instance, JsonDict, Session, URL
from tamr_client.exception import TamrClientException


class InvalidOperation(TamrClientException):
    """Raised when attempting an invalid operation.
    """

    pass


class NotFound(TamrClientException):
    """Raised when referencing a restore that does not exist on the server.
    """

    pass


def _from_json(url: URL, data: JsonDict) -> Restore:
    """Make restore from JSON data (deserialize).

    Args:
        url: Restore url
        data: Restore JSON data from Tamr server
    """
    return Restore(
        url=url,
        backup_path=data["backupPath"],
        state=data["state"],
        error_message=data["errorMessage"],
    )


def get(session: Session, instance: Instance) -> Restore:
    """Get information on the latest Tamr restore, if any.

    Args:
        session: Tamr session
        instance: Tamr instance

    Returns:
        Latest Tamr restore

    Raises:
        restore.NotFound: If no backup found at the specified URL
    """
    url = URL(instance=instance, path="instance/restore")
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    return _from_json(url, response.successful(r).json())


def initiate(session: Session, instance: Instance, backup_path: str) -> Restore:
    """Initiate a Tamr restore.

    Args:
        session: Tamr session
        instance: Tamr instance
        backup_path: Path to the backup

    Returns:
        Initiated restore

    Raises:
        restore.InvalidOperation: If attempting an invalid operation
    """
    url = URL(instance=instance, path="instance/restore")
    r = session.post(str(url), data=backup_path)
    if r.status_code == 400:
        raise InvalidOperation(str(url), r.json()["message"])
    return _from_json(url, response.successful(r).json())


def cancel(session: Session, restore: Restore) -> Restore:
    """Cancel a Tamr restore.

    Args:
        session: Tamr session
        restore: A Tamr restore

    Returns:
        Canceled restore

    Raises:
        restore.NotFound: If no backup file found at the specified path
        restore.InvalidOperation: If attempting an invalid operation
    """
    cancel_url = f"{restore.url}:cancel"
    r = session.post(cancel_url)
    if r.status_code == 404:
        raise NotFound(cancel_url)
    if r.status_code == 400:
        raise InvalidOperation(cancel_url, r.json()["message"])
    return _from_json(restore.url, response.successful(r).json())
