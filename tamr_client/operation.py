"""
See https://docs.tamr.com/new/reference/the-operation-object
"""
from copy import deepcopy
from time import sleep, time as now
from typing import Optional

import requests

from tamr_client import response
from tamr_client._types import Instance, JsonDict, Operation, Session, URL
from tamr_client.exception import TamrClientException


class NotFound(TamrClientException):
    """Raised when referencing an operation that does not exist on the server.
    """

    pass


class Failed(TamrClientException):
    """Raised when checking a failed operation.
    """

    pass


def check(session: Session, operation: Operation):
    """Waits for the operation to finish and raises an exception if the operation was not successful.

    Args:
        operation: Operation to be checked.

    Raises:
        Failed: If the operation failed.
    """
    op = wait(session, operation)
    if not succeeded(op):
        raise Failed(
            f"Checked operation '{str(op.url)}', but it failed with status: {op.status}"
        )


def poll(session: Session, operation: Operation) -> Operation:
    """Poll this operation for server-side updates.

    Does not update the :class:`~tamr_client.operation.Operation` object.
    Instead, returns a new :class:`~tamr_client.operation.Operation`.

    Args:
        operation: Operation to be polled.
    """
    return _by_url(session, operation.url)


def wait(
    session: Session,
    operation: Operation,
    *,
    poll_interval_seconds: int = 3,
    timeout_seconds: Optional[int] = None,
) -> Operation:
    """Continuously polls for this operation's server-side state.

    Args:
        operation: Operation to be polled.
        poll_interval_seconds: Time interval (in seconds) between subsequent polls.
        timeout_seconds: Time (in seconds) to wait for operation to resolve.

    Raises:
        TimeoutError: If operation takes longer than `timeout_seconds` to resolve.
    """
    started = now()
    while timeout_seconds is None or now() - started < timeout_seconds:
        if operation.status is None:
            return operation
        elif operation.status["state"] in ["PENDING", "RUNNING"]:
            sleep(poll_interval_seconds)
        elif operation.status["state"] in ["CANCELED", "SUCCEEDED", "FAILED"]:
            return operation
        operation = poll(session, operation)
    raise TimeoutError(
        f"Waiting for operation took longer than {timeout_seconds} seconds."
    )


def succeeded(operation: Operation) -> bool:
    """Convenience method for checking if operation was successful.
    """
    return operation.status is not None and operation.status["state"] == "SUCCEEDED"


def by_resource_id(session: Session, instance: Instance, resource_id: str) -> Operation:
    """Get operation by ID

    Args:
        resource_id: The ID of the operation
    """
    url = URL(instance=instance, path=f"operations/{resource_id}")
    r = session.get(str(url))
    return _from_response(instance, r)


def _from_response(instance: Instance, response: requests.Response) -> Operation:
    """
    Handle idiosyncrasies in constructing Operations from Tamr responses.
    When a Tamr API call would start an operation, but all results that would be
    produced by that operation are already up-to-date, Tamr returns `HTTP 204 No Content`

    To make it easy for client code to handle these API responses without checking
    the response code, this method will either construct an Operation, or a
    dummy `NoOp` operation representing the 204 Success response.

    Args:
        response: HTTP Response from the request that started the operation.
    """
    if response.status_code == 204:
        # Operation was successful, but the response contains no content.
        # Create a dummy operation to represent this.
        _never = "0000-00-00T00:00:00.000Z"
        _description = """Tamr returned HTTP 204 for this operation, indicating that all
            results that would be produced by the operation are already up-to-date."""
        resource_json = {
            "id": "-1",
            "type": "NOOP",
            "description": _description,
            "status": {
                "state": "SUCCEEDED",
                "startTime": _never,
                "endTime": _never,
                "message": "",
            },
            "created": {"username": "", "time": _never, "version": "-1"},
            "lastModified": {"username": "", "time": _never, "version": "-1"},
            "relativeId": "operations/-1",
        }
    else:
        resource_json = response.json()
    _id = resource_json["id"]
    _url = URL(instance=instance, path=f"operations/{_id}")
    return _from_json(_url, resource_json)


def _by_url(session: Session, url: URL) -> Operation:
    """Get operation by URL

    Fetches operation from Tamr server

    Args:
        url: Operation URL

    Raises:
        operation.NotFound: If no operation could be found at the specified URL.
            Corresponds to a 404 HTTP error.
        requests.HTTPError: If any other HTTP error is encountered.
    """
    r = session.get(str(url))
    if r.status_code == 404:
        raise NotFound(str(url))
    data = response.successful(r).json()
    return _from_json(url, data)


def _from_json(url: URL, data: JsonDict) -> Operation:
    """Make operation from JSON data (deserialize)

    Args:
        url: Operation URL
        data: Operation JSON data from Tamr server
    """
    cp = deepcopy(data)
    return Operation(
        url, type=cp["type"], status=cp.get("status"), description=cp.get("description")
    )
