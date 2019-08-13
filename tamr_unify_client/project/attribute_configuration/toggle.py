from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class Toggle(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("admin", "dt")
        self.unify = Client(auth)

    @responses.activate
    def test_toggle(self):
        project_url = "http://localhost:9100/api/versioned/v1/projects?filter=externalId%3D%3DCharlotte"
        responses.add(responses.GET, project_url, json=self.project_json)

        a_c_url = (
            "http://localhost:9100/api/versioned/v1/projects/1/attributeConfigurations"
        )
        responses.add(responses.GET, a_c_url, json=self.config_json)

        project = self.unify.projects.by_external_id("Charlotte")

        specific_a_c_url = a_c_url + "/1"
        responses.add(responses.GET, specific_a_c_url, json=self.config_json[0])

        all_a_c = list(project.attribute_configurations().stream())
        for config in all_a_c:
            if config.enabled_for_ml:
                build = config.build().with_enabled_for_ml(False)
                print(build._build())

        print("all_a_c")
        print(all_a_c)

        a_c = project.attribute_configurations().by_resource_id("1")
        print("specific a_c")
        print(a_c)

        a_c_ml = a_c.enabled_for_ml
        print(a_c_ml)

        a_c_build = a_c.build().with_enabled_for_ml(False)
        print("build")
        print(a_c_build._build())

    project_json = [
        {
            "id": "unify://unified-data/v1/projects/1",
            "name": "Project_1",
            "description": "Mastering Project",
            "type": "DEDUP",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "created": {
                "username": "admin",
                "time": "2019-06-04T19:55:46.407Z",
                "version": "20",
            },
            "lastModified": {
                "username": "admin",
                "time": "2019-06-21T19:13:26.283Z",
                "version": "2325",
            },
            "relativeId": "projects/1",
            "externalId": "Charlotte",
        }
    ]

    config_json = [
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/1",
            "relativeId": "projects/1/attributeConfigurations/1",
            "relativeAttributeId": "datasets/8/attributes/suburb",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "suburb",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/2",
            "relativeId": "projects/1/attributeConfigurations/2",
            "relativeAttributeId": "datasets/8/attributes/sex",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "sex",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/3",
            "relativeId": "projects/1/attributeConfigurations/3",
            "relativeAttributeId": "datasets/8/attributes/address_2",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "address_2",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/4",
            "relativeId": "projects/1/attributeConfigurations/4",
            "relativeAttributeId": "datasets/8/attributes/age",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "age",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/5",
            "relativeId": "projects/1/attributeConfigurations/5",
            "relativeAttributeId": "datasets/8/attributes/culture",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "culture",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/6",
            "relativeId": "projects/1/attributeConfigurations/6",
            "relativeAttributeId": "datasets/8/attributes/street_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "street_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/7",
            "relativeId": "projects/1/attributeConfigurations/7",
            "relativeAttributeId": "datasets/8/attributes/postcode",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "postcode",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/8",
            "relativeId": "projects/1/attributeConfigurations/8",
            "relativeAttributeId": "datasets/8/attributes/phone_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "phone_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/9",
            "relativeId": "projects/1/attributeConfigurations/9",
            "relativeAttributeId": "datasets/8/attributes/soc_sec_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "soc_sec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/10",
            "relativeId": "projects/1/attributeConfigurations/10",
            "relativeAttributeId": "datasets/8/attributes/rec2_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "rec2_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/11",
            "relativeId": "projects/1/attributeConfigurations/11",
            "relativeAttributeId": "datasets/8/attributes/date_of_birth",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "date_of_birth",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/12",
            "relativeId": "projects/1/attributeConfigurations/12",
            "relativeAttributeId": "datasets/8/attributes/title",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "title",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/13",
            "relativeId": "projects/1/attributeConfigurations/13",
            "relativeAttributeId": "datasets/8/attributes/address_1",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "address_1",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/14",
            "relativeId": "projects/1/attributeConfigurations/14",
            "relativeAttributeId": "datasets/8/attributes/rec_id",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "rec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/15",
            "relativeId": "projects/1/attributeConfigurations/15",
            "relativeAttributeId": "datasets/8/attributes/state",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "state",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/16",
            "relativeId": "projects/1/attributeConfigurations/16",
            "relativeAttributeId": "datasets/8/attributes/family_role",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "family_role",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/17",
            "relativeId": "projects/1/attributeConfigurations/17",
            "relativeAttributeId": "datasets/8/attributes/blocking_number",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "blocking_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/18",
            "relativeId": "projects/1/attributeConfigurations/18",
            "relativeAttributeId": "datasets/8/attributes/surname",
            "attributeRole": "CLUSTER_NAME_ATTRIBUTE",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "surname",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/19",
            "relativeId": "projects/1/attributeConfigurations/19",
            "relativeAttributeId": "datasets/8/attributes/given_name",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": True,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "given_name",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeConfigurations/20",
            "relativeId": "projects/1/attributeConfigurations/20",
            "relativeAttributeId": "datasets/8/attributes/Address1",
            "attributeRole": "",
            "similarityFunction": "COSINE",
            "enabledForMl": False,
            "tokenizer": "DEFAULT",
            "numericFieldResolution": [],
            "attributeName": "Address1",
        },
    ]
