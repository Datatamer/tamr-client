from functools import wraps
import json
import re

import responses


def mock_api(response_log_path):
    """Decorator for `pytest` tests that mocks Unify API.

    :param str response_log_path: Path to mock responses `.ndjson` file

    Usage:
        from .utils import mock_api
        import os
        import requests

        basedir = os.path.dirname(__file__)
        response_log_path = os.path.join(basedir, 'my_mock_responses.ndjson')

        @mock_api(response_log_path)
        def my_test():
            response = request(...)
            assert response.ok
    """

    def wrap(test_func):
        @wraps(test_func)
        @responses.activate
        def wrapped():
            with open(response_log_path) as f:
                for line in f:
                    response = json.loads(line)
                    response["url"] = re.sub(
                        r"(https?:\/\/).*(:9100)", r"\1localhost\2", response["url"]
                    )
                    responses.add(**response)
            test_func()

        return wrapped

    return wrap
