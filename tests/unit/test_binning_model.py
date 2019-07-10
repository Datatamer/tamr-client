from functools import partial
import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


project_config = {
    "name": "Project 1",
    "description": "Mastering Project",
    "type": "DEDUP",
    "unifiedDatasetName": "Project 1 - Unified Dataset",
    "externalId": "Project1",
    "resourceId": "1",
}
project_url = f"http://localhost:9100/api/versioned/v1/projects/1"


@responses.activate
def test_binning_model_records():

    records_body = [
        {
            "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bb8"],
            "isActive": ["true"],
            "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
            "similarityFunction": ["COSINE"],
            "tokenizer": ["DEFAULT"],
            "fieldName": ["surname"],
            "threshold": ["0.75"],
        }
    ]

    records_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/binningModel/records"
    )

    responses.add(responses.GET, project_url, json=project_config)

    responses.add(
        responses.GET,
        records_url,
        body="\n".join(json.dumps(body) for body in records_body),
    )

    unify = Client(UsernamePasswordAuth("username", "password"))

    project = unify.projects.by_resource_id("1").as_mastering()
    binning_model = project.binning_model()

    binning_model_records = list(binning_model.records())
    assert binning_model_records == records_body


@responses.activate
def test_binning_model_update_records():

    records_body = [
        {
            "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bb8"],
            "isActive": ["true"],
            "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
            "similarityFunction": ["COSINE"],
            "tokenizer": ["DEFAULT"],
            "fieldName": ["surname"],
            "threshold": ["0.75"],
        },
        {
            "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bc9"],
            "isActive": ["true"],
            "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
            "similarityFunction": ["COSINE"],
            "tokenizer": ["DEFAULT"],
            "fieldName": ["surname"],
            "threshold": ["0.75"],
        },
        {
            "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bd8"],
            "isActive": ["true"],
            "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
            "similarityFunction": ["COSINE"],
            "tokenizer": ["DEFAULT"],
            "fieldName": ["surname"],
            "threshold": ["0.75"],
        },
    ]

    expected_updates = [
        {
            "action": "CREATE",
            "recordId": "d8b7351d-24ce-49aa-8655-5b5809ab6bb8",
            "record": {
                "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bb8"],
                "isActive": ["true"],
                "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
                "similarityFunction": ["COSINE"],
                "tokenizer": ["DEFAULT"],
                "fieldName": ["surname"],
                "threshold": ["0.75"],
            },
        },
        {
            "action": "CREATE",
            "recordId": "d8b7351d-24ce-49aa-8655-5b5809ab6bc9",
            "record": {
                "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bc9"],
                "isActive": ["true"],
                "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
                "similarityFunction": ["COSINE"],
                "tokenizer": ["DEFAULT"],
                "fieldName": ["surname"],
                "threshold": ["0.75"],
            },
        },
        {
            "action": "CREATE",
            "recordId": "d8b7351d-24ce-49aa-8655-5b5809ab6bd8",
            "record": {
                "id": ["d8b7351d-24ce-49aa-8655-5b5809ab6bd8"],
                "isActive": ["true"],
                "clauseId": ["2e6c5f1b-ed49-40ab-8cbb-350aded25070"],
                "similarityFunction": ["COSINE"],
                "tokenizer": ["DEFAULT"],
                "fieldName": ["surname"],
                "threshold": ["0.75"],
            },
        },
    ]

    snoop_dict = {}

    def update_callback(request, snoop):
        snoop["payload"] = request.body
        return 200, {}, "{}"

    update_records_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/binningModel/records"
    )

    responses.add(responses.GET, project_url, json=project_config)

    responses.add_callback(
        responses.POST,
        update_records_url,
        callback=partial(update_callback, snoop=snoop_dict),
    )

    unify = Client(UsernamePasswordAuth("username", "password"))

    project = unify.projects.by_resource_id("1").as_mastering()
    binning_model = project.binning_model()

    updates = [
        {"action": "CREATE", "recordId": record["id"][0], "record": record}
        for record in records_body
    ]

    binning_model.update_records(updates)
    actual = [json.loads(item) for item in snoop_dict["payload"]]
    assert expected_updates == actual
