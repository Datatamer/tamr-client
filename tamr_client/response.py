import json
import logging
from typing import Iterator

import requests

from tamr_client._types import JsonDict

logger = logging.getLogger(__name__)


def successful(response: requests.Response) -> requests.Response:
    """Ensure response does not contain an HTTP error.

    Delegates to :func:`requests.Response.raise_for_status`

    Returns:
        The response being checked.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error is encountered.
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        r = e.response
        logger.error(
            f"Encountered HTTP error code {r.status_code}. Response body: {r.text}"
        )
        raise e
    return response


def ndjson(response: requests.Response, **kwargs) -> Iterator[JsonDict]:
    """Stream newline-delimited JSON from the response body

    Analog to :func:`requests.Response.json` but for ``.ndjson``-formatted body.

    **Recommended**: For memory efficiency, use ``stream=True`` when sending the request corresponding to this response.

    Args:
        response: Response whose body should be streamed as newline-delimited JSON.
        **kwargs: Keyword arguments passed to underlying :func:`requests.Response.iter_lines` call.

    Returns
        Each line of the response body, parsed as JSON

    Example:
        >>> import tamr_client as tc
        >>> s = tc.session.from_auth(...)
        >>> r = s.get(..., stream=True)
        >>> for data in tc.response.ndjson(r):
        ...     assert data['my key'] == 'my_value'

    """
    for line in response.iter_lines(**kwargs):
        yield json.loads(line)
