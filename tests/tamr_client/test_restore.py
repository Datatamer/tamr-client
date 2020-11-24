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
    data = {
        "id": "unify://unified-data/v1/restore/restore-2020-08-19_20-01-20-233",
        "relativeId": "restore-2020-08-19_20-01-20-233",
        "user": "admin",
        "backupPath": "/home/ubuntu/tamr/backups/2020-08-17_22-07-11-100",
        "state": "CANCELED",
        "stage": "",
        "errorMessage": "",
        "created": "2020-08-19_20-01-20-233",
        "lastModified": "2020-08-19_20-02-19-351",
    }
    restore = tc.restore._from_json(url=tc.URL(path="instance/restore"), data=data)

    tc.restore.cancel(session=s, restore=restore)
