import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_create():
    s = fake.session()
    instance = fake.instance()

    project = tc.schema_mapping.project.create(
        s,
        instance,
        name="New Schema Mapping Project",
        description="A Schema Mapping Project",
    )
    assert isinstance(project, tc.SchemaMappingProject)
    assert project.name == "New Schema Mapping Project"
    assert project.description == "A Schema Mapping Project"
