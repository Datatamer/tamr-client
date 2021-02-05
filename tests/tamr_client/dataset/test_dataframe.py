import pandas as pd
import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_upsert():
    s = fake.session()
    dataset = fake.dataset()

    df = pd.DataFrame(_records_json)

    response = tc.dataframe.upsert(s, dataset, df, primary_key_name="primary_key")
    assert response == _response_json


def test_upsert_primary_key_not_found():
    s = fake.session()
    dataset = fake.dataset()

    df = pd.DataFrame(_records_json)

    with pytest.raises(tc.primary_key.NotFound):
        tc.dataframe.upsert(s, dataset, df, primary_key_name="wrong_primary_key")


@fake.json
def test_upsert_infer_primary_key():
    s = fake.session()
    dataset = fake.dataset()

    df = pd.DataFrame(_records_json)

    response = tc.dataframe.upsert(s, dataset, df)
    assert response == _response_json


@fake.json
def test_upsert_index_as_primary_key():
    s = fake.session()
    dataset = fake.dataset()

    df = pd.DataFrame(
        _records_json_2,
        index=[record["primary_key"] for record in _records_with_keys_json_2],
    )
    df.index.name = "primary_key"

    response = tc.dataframe.upsert(s, dataset, df, primary_key_name="primary_key")
    assert response == _response_json


def test_upsert_index_column_name_collision():
    s = fake.session()
    dataset = fake.dataset()

    df = pd.DataFrame(_records_json_2)
    df.index.name = "primary_key"

    # create column in `df` with same name as index and matching "primary_key"
    df.insert(0, df.index.name, df.index)

    with pytest.raises(tc.primary_key.Ambiguous):
        tc.dataframe.upsert(s, dataset, df, primary_key_name="primary_key")


@fake.json
def test_create():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    dataset = tc.dataframe.create(
        s, instance, df, name="df_dataset", primary_key_name="primary_key"
    )
    assert dataset.name == "df_dataset"
    assert dataset.key_attribute_names == ("primary_key",)


@fake.json
def test_create_infer_primary_key_from_index():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(
        _records_json_2,
        index=[record["primary_key"] for record in _records_with_keys_json_2],
    )
    df.index.name = "primary_key"

    dataset = tc.dataframe.create(s, instance, df, name="df_dataset")
    assert dataset.name == "df_dataset"
    assert dataset.key_attribute_names == ("primary_key",)


def test_create_no_primary_key():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    with pytest.raises(tc.primary_key.NotFound):
        tc.dataframe.create(s, instance, df, name="df_dataset")


def test_create_primary_key_not_found():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    with pytest.raises(tc.primary_key.NotFound):
        tc.dataframe.create(
            s, instance, df, name="df_dataset", primary_key_name="wrong_primary_key"
        )


@fake.json
def test_create_handle_attribute_failure():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    with pytest.raises(tc.dataframe.CreationFailure):
        tc.dataframe.create(
            s, instance, df, name="df_dataset", primary_key_name="primary_key"
        )


@fake.json
def test_create_deletion_failure():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    with pytest.raises(tc.dataframe.CreationFailure):
        tc.dataframe.create(
            s, instance, df, name="df_dataset", primary_key_name="primary_key"
        )


@fake.json
def test_create_handle_record_failure():
    s = fake.session()
    instance = fake.instance()

    df = pd.DataFrame(_records_with_keys_json_2)

    with pytest.raises(tc.dataframe.CreationFailure):
        tc.dataframe.create(
            s, instance, df, name="df_dataset", primary_key_name="primary_key"
        )


_records_json = [{"primary_key": 1}, {"primary_key": 2}]

_records_json_2 = [{"attribute": 1}, {"attribute": 2}]

_records_with_keys_json_2 = [
    {"primary_key": 1, "attribute": 1},
    {"primary_key": 2, "attribute": 2},
]

_response_json = {
    "numCommandsProcessed": 2,
    "allCommandsSucceeded": True,
    "validationErrors": [],
}
