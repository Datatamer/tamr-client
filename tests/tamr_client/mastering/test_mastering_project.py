import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_create():
    s = fake.session()
    instance = fake.instance()

    project = tc.mastering.project.create(
        s, instance, name="New Mastering Project", description="A Mastering Project"
    )
    assert isinstance(project, tc.MasteringProject)
    assert project.name == "New Mastering Project"
    assert project.description == "A Mastering Project"
