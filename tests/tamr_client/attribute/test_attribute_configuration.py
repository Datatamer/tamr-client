from typing import List, Tuple

import pytest

import tamr_client as tc
from tests.tamr_client import fake


_attribute_configuration_json = {
    "id": "unify://unified-data/v1/projects/1/attributeConfigurations/1600",
    "relativeId": "projects/1/attributeConfigurations/1600",
    "relativeAttributeId": "datasets/1/attributes/street_address",
    "attributeRole": "",
    "similarityFunction": "COSINE",
    "enabledForMl": True,
    "tokenizer": "DEFAULT",
    "numericFieldResolution": [],
    "attributeName": "StreetAddress",
}

AttributeRole = tc.attribute.configuration.AttributeRole
SimilarityFunction = tc.attribute.configuration.SimilarityFunction
Tokenizer = tc.attribute.configuration.Tokenizer


@fake.json
def test_by_resource_id():
    s = fake.session()
    project = fake.mastering_project()

    attribute_conf = tc.attribute.configuration.by_resource_id(s, project, "1600")

    assert isinstance(attribute_conf, tc.AttributeConfiguration)
    assert attribute_conf.attribute_role is AttributeRole.NONE
    assert attribute_conf.similarity_function == SimilarityFunction.COSINE
    assert attribute_conf.enabled_for_ml
    assert attribute_conf.tokenizer == Tokenizer.DEFAULT
    assert attribute_conf.numeric_field_resolution == []
    assert isinstance(attribute_conf.attribute, tc.Attribute)
    assert attribute_conf.attribute.name == "StreetAddress"


@fake.json
def test_create():
    s = fake.session()
    project = fake.mastering_project()
    attribute = fake.project_attribute()

    attribute_conf = tc.attribute.configuration.create(
        s,
        project,
        unified_attribute=attribute,
        attribute_role=tc.attribute.configuration.AttributeRole.CLUSTER_NAME_ATTRIBUTE,
        similarity_function=tc.attribute.configuration.SimilarityFunction.COSINE,
        enabled_for_ml=True,
        tokenizer=tc.attribute.configuration.Tokenizer.DEFAULT,
        numeric_field_resolution=None,
    )

    assert isinstance(attribute_conf, tc.AttributeConfiguration)
    assert attribute_conf.attribute_role == AttributeRole.CLUSTER_NAME_ATTRIBUTE
    assert attribute_conf.similarity_function == SimilarityFunction.COSINE
    assert attribute_conf.enabled_for_ml
    assert attribute_conf.tokenizer == Tokenizer.DEFAULT
    assert attribute_conf.numeric_field_resolution == []
    assert attribute_conf.attribute == attribute


@fake.json
def test_create_numeric():
    s = fake.session()
    project = fake.mastering_project()
    attribute = fake.project_attribute()

    attribute_conf = tc.attribute.configuration.create(
        s,
        project,
        unified_attribute=attribute,
        similarity_function=tc.attribute.configuration.SimilarityFunction.ABSOLUTE_DIFF,
        enabled_for_ml=True,
    )

    assert isinstance(attribute_conf, tc.AttributeConfiguration)
    assert attribute_conf.attribute_role == AttributeRole.NONE
    assert attribute_conf.similarity_function == SimilarityFunction.ABSOLUTE_DIFF
    assert attribute_conf.enabled_for_ml
    assert attribute_conf.tokenizer == Tokenizer.NONE
    assert attribute_conf.numeric_field_resolution == []
    assert attribute_conf.attribute == attribute


def test_create_bad_parameters():
    param_sets: List[Tuple[SimilarityFunction, Tokenizer, List[int]]] = [
        (SimilarityFunction.COSINE, Tokenizer.DEFAULT, [1]),
        (SimilarityFunction.COSINE, Tokenizer.NONE, []),
        (SimilarityFunction.ABSOLUTE_DIFF, Tokenizer.DEFAULT, []),
    ]
    s = fake.session()
    project = fake.mastering_project()
    attribute = fake.project_attribute()
    for param in param_sets:
        with pytest.raises(tc.attribute.configuration.Invalid):
            tc.attribute.configuration.create(
                s,
                project,
                unified_attribute=attribute,
                similarity_function=param[0],
                tokenizer=param[1],
                numeric_field_resolution=param[2],
            )


@fake.json
def test_get_all():
    s = fake.session()
    project = fake.mastering_project()

    attribute_confs = tc.attribute.configuration.get_all(s, project)
    assert len(attribute_confs) == 2

    attribute_conf = attribute_confs[1]
    assert isinstance(attribute_conf, tc.AttributeConfiguration)
    assert attribute_conf.attribute_role == AttributeRole.NONE
    assert attribute_conf.similarity_function == SimilarityFunction.JACCARD
    assert attribute_conf.enabled_for_ml
    assert attribute_conf.tokenizer == Tokenizer.BIWORD
    assert attribute_conf.numeric_field_resolution == []
    assert isinstance(attribute_conf.attribute, tc.Attribute)
    assert attribute_conf.attribute.name == "StreetAddress2"


@fake.json
def test_update():
    s = fake.session()
    attribute_conf = fake.attribute_configuration()
    updated_attr_conf = tc.attribute.configuration.update(
        s,
        attribute_conf,
        attribute_role=tc.attribute.configuration.AttributeRole.SUM_ATTRIBUTE,
        similarity_function=tc.attribute.configuration.SimilarityFunction.ABSOLUTE_DIFF,
        numeric_field_resolution=[10],
    )

    assert isinstance(updated_attr_conf, tc.AttributeConfiguration)
    assert updated_attr_conf.attribute_role == AttributeRole.SUM_ATTRIBUTE
    assert updated_attr_conf.similarity_function == SimilarityFunction.ABSOLUTE_DIFF
    assert updated_attr_conf.enabled_for_ml
    assert updated_attr_conf.tokenizer == Tokenizer.NONE
    assert updated_attr_conf.numeric_field_resolution == [10]
    assert isinstance(updated_attr_conf.attribute, tc.Attribute)
    assert updated_attr_conf.attribute.name == "StreetAddress"


@fake.json
def test_delete():
    s = fake.session()
    attribute_conf = fake.attribute_configuration()
    tc.attribute.configuration.delete(s, attribute_conf)


@fake.json
def test_by_resource_id_attribute_configuration_not_found():
    s = fake.session()
    project = fake.mastering_project()

    with pytest.raises(tc.attribute.configuration.NotFound):
        tc.attribute.configuration.by_resource_id(s, project, "1600")


@fake.json
def test_create_attribute_configuration_exists():
    s = fake.session()
    project = fake.mastering_project()
    attribute = fake.project_attribute()

    with pytest.raises(tc.attribute.configuration.AlreadyExists):
        tc.attribute.configuration.create(s, project, unified_attribute=attribute)


@fake.json
def test_update_attribute_configuration_not_found():
    s = fake.session()
    attribute_conf = fake.attribute_configuration()

    with pytest.raises(tc.attribute.configuration.NotFound):
        tc.attribute.configuration.update(
            s, attribute_conf,
        )
