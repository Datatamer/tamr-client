import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_manual_labels():
    s = fake.session()
    instance = fake.instance()
    project = fake.categorization_project()

    tc.categorization.project.manual_labels(
        session=s, instance=instance, project=project
    )
