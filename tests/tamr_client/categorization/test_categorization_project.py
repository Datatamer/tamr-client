import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_create():
    s = fake.session()
    instance = fake.instance()

    project = tc.categorization.project.create(
        s,
        instance,
        name="New Categorization Project",
        description="A Categorization Project",
    )
    assert isinstance(project, tc.CategorizationProject)
    assert project.name == "New Categorization Project"
    assert project.description == "A Categorization Project"
