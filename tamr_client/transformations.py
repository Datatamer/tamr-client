import requests

from tamr_client import dataset, response
from tamr_client._types import (
    InputTransformation,
    Instance,
    JsonDict,
    Project,
    Session,
    Transformations,
)


def _input_transformation_from_json(
    session: Session, instance: Instance, data: JsonDict
) -> InputTransformation:
    """Make input transformation from JSON data (deserialize)

    Args:
        instance: Tamr instance containing this transformation
        data: Input scoped transformation JSON data from Tamr server
    """
    dataset_resource_ids = [d["datasetId"].split("/")[-1] for d in data["datasets"]]
    datasets = [
        dataset.by_resource_id(session, instance, d_id) for d_id in dataset_resource_ids
    ]
    return InputTransformation(transformation=data["transformation"], datasets=datasets)


def _from_json(session: Session, instance: Instance, data: JsonDict) -> Transformations:
    """Make transformations from JSON data (deserialize)

    Args:
        instance: Tamr instance containing this transformation
        data: Transformation JSON data from Tamr server
    """
    return Transformations(
        unified_scope=data["unified"],
        input_scope=[
            _input_transformation_from_json(session, instance, tx)
            for tx in data["parameterized"]
        ],
    )


def _input_transformation_to_json(tx: InputTransformation) -> JsonDict:
    """Convert input transformations to JSON data (serialize)

    Args:
        tx: Input transformation to convert
    """
    # datasetId omitted, only one of "datasetId" or "relativeDatasetId" is required
    dataset_json = [
        {"name": d.name, "relativeDatasetId": d.url.path} for d in tx.datasets
    ]

    return {"datasets": dataset_json, "transformation": tx.transformation}


def _to_json(tx: Transformations) -> JsonDict:
    """Convert transformations to JSON data (serialize)

    Args:
        tx: Transformations to convert
    """
    return {
        "parameterized": [_input_transformation_to_json(t) for t in tx.input_scope],
        "unified": tx.unified_scope,
    }


def get_all(session: Session, project: Project) -> Transformations:
    """Get the transformations of a Project

    Args:
        project: Project containing transformations

    Raises:
        requests.HTTPError: If any HTTP error is encountered.

    Example:
        >>> import tamr_client as tc
        >>> session = tc.session.from_auth('username', 'password')
        >>> instance = tc.instance.Instance(host="localhost", port=9100)
        >>> project1 = tc.project.by_resource_id(session, instance, id='1')
        >>> print(tc.transformations.get_all(session, project1))
    """
    r = session.get(f"{project.url}/transformations")
    response.successful(r)
    return _from_json(session, project.url.instance, r.json())


def replace_all(
    session: Session, project: Project, tx: Transformations
) -> requests.Response:
    """Replaces the transformations of a Project

    Args:
        project: Project to place transformations within
        tx: Transformations to put into project

    Raises:
        requests.HTTPError: If any HTTP error is encountered.

    Example:
        >>> import tamr_client as tc
        >>> session = tc.session.from_auth('username', 'password')
        >>> instance = tc.instance.Instance(host="localhost", port=9100)
        >>> project1 = tc.project.by_resource_id(session, instance, id='1')
        >>> dataset3 = tc.dataset.by_resource_id(session, instance, id='3')
        >>> new_input_tx = tc.InputTransformation("SELECT *, upper(name) as name;", [dataset3])
        >>> all_tx = tc.Transformations(
        ... input_scope=[new_input_tx],
        ... unified_scope=["SELECT *, 1 as one;"]
        ... )
        >>> tc.transformations.replace_all(session, project1, all_tx)
    """
    body = _to_json(tx)
    r = session.put(f"{project.url}/transformations", json=body)

    return response.successful(r)
