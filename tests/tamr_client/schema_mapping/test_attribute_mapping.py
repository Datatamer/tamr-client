import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_create():
    s = fake.session()
    project = fake.schema_mapping_project()
    input_attribute = fake.attribute()
    unified_attribute = _unified_attribute

    mapping = tc.schema_mapping.attribute_mapping.create(
        s,
        project,
        input_attribute=input_attribute,
        unified_attribute=unified_attribute,
    )
    assert isinstance(mapping, tc.AttributeMapping)
    assert mapping.input_attribute == input_attribute
    assert mapping.unified_attribute == unified_attribute


@fake.json
def test_create_already_exists():
    s = fake.session()
    project = fake.schema_mapping_project()
    input_attribute = fake.attribute()
    unified_attribute = _unified_attribute

    with pytest.raises(tc.schema_mapping.attribute_mapping.AlreadyExists):
        tc.schema_mapping.attribute_mapping.create(
            s,
            project,
            input_attribute=input_attribute,
            unified_attribute=unified_attribute,
        )


@fake.json
def test_create_ambiguous():
    s = fake.session()
    project = fake.schema_mapping_project()
    input_attribute = tc.Attribute(
        url=tc.URL(path="datasets/1/attributes/BadAttribute"),
        name="BadAttribute",
        type=tc.attribute.type.DEFAULT,
        description="Not an existing attribute",
        is_nullable=False,
    )
    unified_attribute = _unified_attribute

    with pytest.raises(tc.schema_mapping.attribute_mapping.Ambiguous):
        tc.schema_mapping.attribute_mapping.create(
            s,
            project,
            input_attribute=input_attribute,
            unified_attribute=unified_attribute,
        )


@fake.json
def test_create_dataset_not_found():
    s = fake.session()
    project = fake.schema_mapping_project()
    input_attribute = fake.attribute()
    unified_attribute = tc.Attribute(
        url=tc.URL(path="datasets/9/attributes/SourceRowNum"),
        name="SourceRowNum",
        type=tc.attribute.type.DEFAULT,
        description="Synthetic row number",
        is_nullable=False,
    )

    with pytest.raises(tc.dataset.NotFound):
        tc.schema_mapping.attribute_mapping.create(
            s,
            project,
            input_attribute=input_attribute,
            unified_attribute=unified_attribute,
        )


@fake.json
def test_create_project_not_found():
    s = fake.session()
    project = tc.SchemaMappingProject(
        tc.URL(path="projects/9"),
        name="Project 4",
        description="A nonexistent Schema Mapping Project",
    )
    input_attribute = fake.attribute()
    unified_attribute = _unified_attribute

    with pytest.raises(tc.project.NotFound):
        tc.schema_mapping.attribute_mapping.create(
            s,
            project,
            input_attribute=input_attribute,
            unified_attribute=unified_attribute,
        )


@fake.json
def test_get_all():
    s = fake.session()
    project = fake.schema_mapping_project()

    mappings = tc.schema_mapping.attribute_mapping.get_all(s, project)

    assert len(mappings) == 2

    mapping_1 = mappings[0]
    assert isinstance(mapping_1, tc.AttributeMapping)
    assert mapping_1.input_attribute == fake.attribute()
    assert mapping_1.unified_attribute == _unified_attribute

    mapping_2 = mappings[1]
    assert isinstance(mapping_2, tc.AttributeMapping)
    assert mapping_2.input_attribute == fake.attribute()
    assert mapping_2.unified_attribute == _unified_attribute_2


@fake.json
def test_delete():
    s = fake.session()
    mapping = fake.attribute_mapping()

    tc.schema_mapping.attribute_mapping.delete(s, mapping)


@fake.json
def test_delete_not_found():
    s = fake.session()
    bad_mapping = tc.AttributeMapping(
        url=tc.URL(path="projects/4/attributeMappings/000-000"),
        input_attribute=fake.attribute(),
        unified_attribute=_unified_attribute,
    )

    with pytest.raises(tc.schema_mapping.attribute_mapping.NotFound):
        tc.schema_mapping.attribute_mapping.delete(s, bad_mapping)


_unified_attribute = tc.Attribute(
    url=tc.URL(path="datasets/2/attributes/SourceRowNum"),
    name="SourceRowNum",
    type=tc.attribute.type.DEFAULT,
    description="Synthetic row number",
    is_nullable=False,
)

_unified_attribute_2 = tc.Attribute(
    url=tc.URL(path="datasets/2/attributes/OtherSourceRowNum"),
    name="OtherSourceRowNum",
    type=tc.attribute.type.DEFAULT,
    description="Synthetic row number",
    is_nullable=False,
)
