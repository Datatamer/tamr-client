import os

from .utils import response_logger, log_entry
from unify_api_v1.auth import UsernamePasswordAuth
import unify_api_v1 as api

basedir = os.path.dirname(__file__)
response_log_path = os.path.join(
    basedir, "../response_logs/continuous_categorization.ndjson"
)


def test_continuous_categorization():
    username = os.environ["UNIFY_USERNAME"]
    password = os.environ["UNIFY_PASSWORD"]
    auth = UsernamePasswordAuth(username, password)

    host = os.environ.get("UNIFY_HOST", "localhost")
    unify = api.Client(auth, host=host)

    unify.logger = response_logger(response_log_path)
    unify.log_entry = log_entry

    project_id = "3"
    project = unify.projects.by_resource_id(project_id)
    project = project.as_categorization()

    unified_dataset = project.unified_dataset()
    op = unified_dataset.refresh()
    assert op.succeeded()

    model = project.model()
    op = model.train()
    assert op.succeeded()

    op = model.predict()
    assert op.succeeded()
