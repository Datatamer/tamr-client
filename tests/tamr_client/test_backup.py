import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_get_all():
    s = fake.session()
    instance = fake.instance()

    tc.backup.get_all(session=s, instance=instance)


@fake.json
def test_by_resource_id():
    s = fake.session()
    instance = fake.instance()
    resource_id = "2020-08-17_21-32-10-961"

    tc.backup.by_resource_id(session=s, instance=instance, resource_id=resource_id)


@fake.json
def test_initiate():
    s = fake.session()
    instance = fake.instance()

    tc.backup.initiate(session=s, instance=instance)


@fake.json
def test_cancel():
    s = fake.session()
    data = {
        "id": "unify://unified-data/v1/backups/2020-08-17_21-32-10-961",
        "relativeId": "2020-08-17_21-32-10-961",
        "user": "admin",
        "backupPath": "/home/ubuntu/tamr/backups/2020-08-17_21-32-10-961",
        "state": "RUNNING",
        "stage": "",
        "errorMessage": "",
        "created": "2020-08-17_21-32-10-961",
        "lastModified": "2020-08-17_21-51-57-600",
    }
    backup = tc.backup._from_json(
        url=tc.URL(path="backups/2020-08-17_21-32-10-961"), data=data
    )

    tc.backup.cancel(session=s, backup=backup)


@fake.json
def test_poll():
    s = fake.session()
    data = {
        "id": "unify://unified-data/v1/backups/2020-08-17_21-32-10-961",
        "relativeId": "2020-08-17_21-32-10-961",
        "user": "admin",
        "backupPath": "/home/ubuntu/tamr/backups/2020-08-17_21-32-10-961",
        "state": "RUNNING",
        "stage": "",
        "errorMessage": "",
        "created": "2020-08-17_21-32-10-961",
        "lastModified": "2020-08-17_21-51-57-600",
    }
    backup = tc.backup._from_json(
        url=tc.URL(path="backups/2020-08-17_21-32-10-961"), data=data
    )

    tc.backup.poll(session=s, backup=backup)
