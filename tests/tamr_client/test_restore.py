import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_get():
    s = fake.session()
    instance = fake.instance()

    tc.restore.get(session=s, instance=instance)


@fake.json
def test_initiate():
    s = fake.session()
    instance = fake.instance()
    backup_path = "2020-08-19_20-01-20-233"

    tc.restore.initiate(session=s, instance=instance, backup_path=backup_path)


@fake.json
def test_cancel():
    s = fake.session()
    instance = fake.instance()

    tc.restore.cancel(session=s, instance=instance)
