import os

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from .utils import mock_api

basedir = os.path.dirname(__file__)
response_log_path = os.path.join(
    basedir, "../response_logs/continuous_mastering.ndjson"
)


@mock_api(response_log_path)
def test_continuous_mastering():
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)

    project_id = "1"
    project = unify.projects.by_resource_id(project_id)
    project = project.as_mastering()

    unified_dataset = project.unified_dataset()
    op = unified_dataset.refresh(poll_interval_seconds=0)
    assert op.succeeded()

    op = project.pairs().refresh(poll_interval_seconds=0)
    assert op.succeeded()

    model = project.pair_matching_model()
    op = model.train(poll_interval_seconds=0)
    assert op.succeeded()

    op = model.predict(poll_interval_seconds=0)
    assert op.succeeded()

    op = project.published_clusters().refresh(poll_interval_seconds=0)
    assert op.succeeded()
