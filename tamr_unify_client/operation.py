from time import sleep, time as now

from tamr_unify_client.base_resource import BaseResource


class Operation(BaseResource):
    """A long-running operation performed by Tamr.
    Operations appear on the "Jobs" page of the Tamr UI.

    By design, client-side operations represent server-side operations *at a
    particular point in time* (namely, when the operation was fetched from the
    server). In other words: Operations *will not* pick up on server-side
    changes automatically. To get an up-to-date representation, refetch the
    operation e.g. ``op = op.poll()``.
    """

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    @classmethod
    def from_resource_id(cls, client, resource_id):
        """Get an operation by resource ID.

        :param client: Delegate underlying API calls to this client.
        :type client: :class:`~tamr_unify_client.Client`
        :param resource_id: The ID of the operation
        :type resource_id: str
        :returns: The specified operation
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        url = f"operations/{resource_id}"
        response = client.get(url).successful()
        return Operation.from_response(client, response)

    @classmethod
    def from_response(cls, client, response):
        """
        Handle idiosyncrasies in constructing Operations from Tamr responses.
        When a Tamr API call would start an operation, but all results that would be
        produced by that operation are already up-to-date, Tamr returns `HTTP 204 No Content`

        To make it easy for client code to handle these API responses without checking
        the response code, this method will either construct an Operation, or a
        dummy `NoOp` operation representing the 204 Success response.

        :param client: Delegate underlying API calls to this client.
        :type client: :class:`~tamr_unify_client.Client`
        :param response: HTTP Response from the request that started the operation.
        :type response: :class:`requests.Response`
        :return: Operation
        :rtype: :class:`~tamr_unify_client.operation.Operation`
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
        return Operation.from_json(client, resource_json)

    def apply_options(self, asynchronous=False, **options):
        """Applies operation options to this operation.

        **NOTE**: This function **should not** be called directly. Rather, options should be
        passed in through a higher-level function e.g. :func:`~tamr_unify_client.dataset.resource.Dataset.refresh` .

        Synchronous mode:
            Automatically waits for operation to resolve before returning the
            operation.

        asynchronous mode:
            Immediately return the ``'PENDING'`` operation. It is
            up to the user to coordinate this operation with their code via
            :func:`~tamr_unify_client.operation.Operation.wait` and/or
            :func:`~tamr_unify_client.operation.Operation.poll` .

        :param asynchronous: Whether or not to run in asynchronous mode. Default: ``False``.
        :type asynchronous: bool
        :param ``**options``: When running in synchronous mode, these options are
            passed to the underlying :func:`~tamr_unify_client.operation.Operation.wait` call.
        :return: Operation with options applied.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        if asynchronous:
            return self
        return self.wait(**options)

    @property
    def type(self):
        """:type: str"""
        return self._data.get("type")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def status(self):
        return self._data.get("status")

    @property
    def state(self):
        """Server-side state of this operation.

        Operation state can be unresolved (i.e. ``state`` is one of: ``'PENDING'``, ``'RUNNING'``),
        or resolved (i.e. `state` is one of: ``'CANCELED'``, ``'SUCCEEDED'``, ``'FAILED'``).
        Unless opting into asynchronous mode, all exposed operations should be resolved.

        Note: you only need to manually pick up server-side changes when opting into asynchronous mode when kicking off this operation.

        Usage:
            >>> op.state # operation is currently 'PENDING'
            'PENDING'
            >>> op.wait() # continually polls until operation resolves
            >>> op.state # incorrect usage; operation object state never changes.
            'PENDING'
            >>> op = op.poll() # correct usage; use value returned by Operation.poll or Operation.wait
            >>> op.state
            'SUCCEEDED'
        """
        return (self.status or {}).get("state")

    def poll(self):
        """Poll this operation for server-side updates.

        Does not update the calling :class:`~tamr_unify_client.operation.Operation` object.
        Instead, returns a new :class:`~tamr_unify_client.operation.Operation`.

        :return: Updated representation of this operation.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        op_json = self.client.get(self.api_path).successful().json()
        return Operation.from_json(self.client, op_json)

    def wait(self, poll_interval_seconds=3, timeout_seconds=None):
        """Continuously polls for this operation's server-side state.

        :param int poll_interval_seconds: Time interval (in seconds) between subsequent polls.
        :param int timeout_seconds: Time (in seconds) to wait for operation to resolve.
        :raises TimeoutError: If operation takes longer than `timeout_seconds` to resolve.
        :return: Resolved operation.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        started = now()
        op = self
        while timeout_seconds is None or now() - started < timeout_seconds:
            if op.state in ["PENDING", "RUNNING"]:
                sleep(poll_interval_seconds)
            elif op.state in ["CANCELED", "SUCCEEDED", "FAILED"]:
                return op
            op = op.poll()
        raise TimeoutError(
            f"Waiting for operation took longer than {timeout_seconds} seconds."
        )

    def succeeded(self):
        """Convenience method for checking if operation was successful.

        :return: ``True`` if operation's state is ``'SUCCEEDED'``, ``False`` otherwise.
        :rtype: :py:class:`bool`
        """
        return self.state == "SUCCEEDED"

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"description={self.description!r}, "
            f"state={self.state!r})"
        )
