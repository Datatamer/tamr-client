from .utils import mock_api
import os

from tamr_unify_client.auth import UsernamePasswordAuth
import tamr_unify_client as api


basedir = os.path.dirname(__file__)
response_log_path = os.path.join(
    basedir, "../response_logs/continuous_categorization.ndjson"
)


@mock_api(response_log_path)
def test_continuous_categorization():
    auth = UsernamePasswordAuth("username", "password")
    unify = api.Client(auth)

    project_id = "3"
    project = unify.projects.by_resource_id(project_id)
    project = project.as_categorization()

    unified_dataset = project.unified_dataset()
    op = unified_dataset.refresh(poll_interval_seconds=0)
    assert op.succeeded()

    model = project.model()
    op = model.train(poll_interval_seconds=0)
    assert op.succeeded()

    op = model.predict(poll_interval_seconds=0)
    assert op.succeeded()
