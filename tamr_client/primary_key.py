class Ambiguous(Exception):
    """Raised when referencing a primary key by name that matches multiple possible targets."""

    pass


class NotFound(Exception):
    """Raised when referencing a primary key by name that does not exist."""

    pass
