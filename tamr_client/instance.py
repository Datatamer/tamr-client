from tamr_client._types import Instance, Session


def origin(instance: Instance) -> str:
    """HTTP origin i.e. :code:`<protocol>://<host>[:<port>]`.

    For additional information, see `MDN web docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_ .
    """
    if instance.port is None:
        return f"{instance.protocol}://{instance.host}"
    else:
        return f"{instance.protocol}://{instance.host}:{instance.port}"


def version(session: Session, instance: Instance) -> str:
    """Return the Tamr version for an instance.

    Args:
        session: Tamr Session
        instance: Tamr instance

    Returns: Version

    """
    # Version endpoints are not themselves versioned by design, but they are stable so they are ok to use here.
    return session.get(f"{origin(instance)}/api/versioned/service/version").json()[
        "version"
    ]
