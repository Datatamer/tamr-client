import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_by_resource_id():
    s = fake.session()
    instance = fake.instance()

    dataset = tc.dataset.by_resource_id(s, instance, "1")
    assert dataset.name == "dataset 1 name"
    assert dataset.description == "dataset 1 description"
    assert dataset.key_attribute_names == ("tamr_id",)


@fake.json
def test_by_resource_id_dataset_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.dataset.NotFound):
        tc.dataset.by_resource_id(s, instance, "1")


@fake.json
def test_by_name():
    s = fake.session()
    instance = fake.instance()

    dataset = tc.dataset.by_name(s, instance, "dataset 1 name")
    assert dataset.name == "dataset 1 name"
    assert dataset.description == "dataset 1 description"
    assert dataset.key_attribute_names == ("tamr_id",)


@fake.json
def test_by_name_dataset_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.dataset.NotFound):
        tc.dataset.by_name(s, instance, "missing dataset")


@fake.json
def test_by_name_dataset_ambiguous():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.dataset.Ambiguous):
        tc.dataset.by_name(s, instance, "ambiguous dataset")


@fake.json
def test_attributes():
    s = fake.session()
    dataset = fake.dataset()

    attrs = tc.dataset.attributes(s, dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert row_num.type == tc.attribute.type.STRING

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute.type.Record)


@fake.json
def test_materialize_async():
    s = fake.session()
    dataset = fake.dataset()

    op = tc.dataset._materialize_async(s, dataset)

    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_delete():
    s = fake.session()
    dataset = fake.dataset()

    tc.dataset.delete(s, dataset)


@fake.json
def test_delete_cascading():
    s = fake.session()
    dataset = fake.dataset()

    tc.dataset.delete(s, dataset, cascade=True)


@fake.json
def test_delete_dataset_not_found():
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.dataset.NotFound):
        tc.dataset.delete(s, dataset)


@fake.json
def test_get_all():
    s = fake.session()
    instance = fake.instance()

    all_datasets = tc.dataset.get_all(s, instance)
    assert len(all_datasets) == 2

    dataset_1 = all_datasets[0]
    assert dataset_1.name == "dataset 1 name"
    assert dataset_1.description == "dataset 1 description"
    assert dataset_1.key_attribute_names == ("tamr_id",)

    dataset_2 = all_datasets[1]
    assert dataset_2.name == "dataset 2 name"
    assert dataset_2.description == "dataset 2 description"
    assert dataset_2.key_attribute_names == ("tamr_id",)


@fake.json
def test_get_all_filter():
    s = fake.session()
    instance = fake.instance()

    all_datasets = tc.dataset.get_all(
        s, instance, filter="description==dataset 2 description"
    )
    assert len(all_datasets) == 1

    dataset = all_datasets[0]
    assert dataset.name == "dataset 2 name"
    assert dataset.description == "dataset 2 description"
    assert dataset.key_attribute_names == ("tamr_id",)


@fake.json
def test_get_all_filter_list():
    s = fake.session()
    instance = fake.instance()

    all_datasets = tc.dataset.get_all(
        s,
        instance,
        filter=["description==dataset 2 description", "version==dataset 2 version"],
    )
    assert len(all_datasets) == 1

    dataset = all_datasets[0]
    assert dataset.name == "dataset 2 name"
    assert dataset.description == "dataset 2 description"
    assert dataset.key_attribute_names == ("tamr_id",)
