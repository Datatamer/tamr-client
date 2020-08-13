from tamr_client.exception import TamrClientException


class Ambiguous(TamrClientException):
    """Raised when referencing a primary key by name that matches multiple possible targets."""

    pass


class NotFound(TamrClientException):
    """Raised when referencing a primary key by name that does not exist."""

    pass
