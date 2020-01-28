import logging

import requests

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


# monkey-patch requests.Response.successful
requests.Response.successful = successful  # type: ignore
