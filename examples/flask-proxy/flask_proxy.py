import json
from typing import Any, Callable

from flask import request, Response
import requests

from tamr_unify_client import Client


def proxy(tamr: Client):
    """Proxy requests in Flask app to Tamr API.

    Adapted from https://stackoverflow.com/a/36601467/1490091

    Args:
        tamr: Proxy requests via this Tamr Client

    Returns:
        Function `(*args, **kwargs) -> requests.Response`

    Example:
        Intercept a specific API endpoint to do some processing on it::

            passthru = proxy(tamr)
            app = Flask(__name__)

            @app.route("/api/endpoint/to/intercept")
            def some_route(*args, **kwargs):
                # specially process this endpoint before passing it through to Tamr server
                print('this endpoint was called!')
                return passthru(*args, **kwargs)

            # all other endpoints, passthru without doing anything special
            app.route("/api/<path:path>", methods=["POST", "GET", "PUT", "DELETE"])(passthru)
    """

    def _proxy(*args: Any, **kwargs: Any) -> Response:
        """Translates Flask's werkzeug.wrappers.Request to Tamr Client's
        requests.Request and send that request to Tamr Client's host.

        Returns:
            Response from Tamr server.
        """
        r = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, tamr.origin + "/"),
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        ]
        headers = [
            (name, value)
            for (name, value) in r.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(
            r.iter_content(chunk_size=10 * 1024),
            r.status_code,
            headers,
            content_type=r.headers.get("Content-Type"),
        )

    return _proxy
