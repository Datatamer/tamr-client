from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.resource import Project


class TestProject(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_project_add_input_dataset(self):
        responses.add(responses.GET, self.datasets_url, json=self.dataset_json)
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.POST,
            self.input_datasets_url,
            json=self.post_input_datasets_json,
            status=204,
        )
        responses.add(
            responses.GET, self.input_datasets_url, json=self.get_input_datasets_json
        )

        dataset = self.tamr.datasets.by_external_id(self.dataset_external_id)
        project = self.tamr.projects.by_external_id(self.project_external_id)
        project.add_input_dataset(dataset)
        alias = project.api_path + "/inputDatasets"
        input_datasets = project.client.get(alias).successful().json()
        self.assertEqual(self.dataset_json, input_datasets)

    @responses.activate
    def test_project_remove_input_dataset(self):
        dataset_id = self.dataset_json[0]["relativeId"]

        responses.add(responses.GET, self.input_datasets_url, json=self.dataset_json)
        responses.add(
            responses.DELETE, f"{self.input_datasets_url}?id={dataset_id}", status=204
        )
        responses.add(responses.GET, self.input_datasets_url, json=[])

        project = Project(self.tamr, self.project_json[0])
        dataset = next(project.input_datasets().stream())

        response = project.remove_input_dataset(dataset)
        self.assertEqual(response.status_code, 204)

        input_datasets = project.input_datasets()
        self.assertEqual(list(input_datasets), [])

    @responses.activate
    def test_project_by_external_id__raises_when_not_found(self):
        responses.add(responses.GET, self.projects_url, json=[])
        with self.assertRaises(KeyError):
            self.tamr.projects.by_external_id(self.project_external_id)

    @responses.activate
    def test_project_by_external_id_succeeds(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        actual_project = self.tamr.projects.by_external_id(self.project_external_id)
        self.assertEqual(self.project_json[0], actual_project._data)

    @responses.activate
    def test_project_attributes_get(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.GET,
            self.project_attributes_url,
            json=self.project_attributes_json,
        )
        project = self.tamr.projects.by_external_id(self.project_external_id)
        attributes = list(project.attributes)
        self.assertEqual(len(self.project_attributes_json), len(attributes))

        responses.add(
            responses.GET,
            self.project_attributes_url + "/id",
            json=self.project_attributes_json[0],
        )
        id_attribute = project.attributes.by_name("id")
        self.assertEqual(self.project_attributes_json[0]["name"], id_attribute.name)

    @responses.activate
    def test_project_attributes_post(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.GET,
            self.project_attributes_url,
            json=self.project_attributes_json,
        )
        responses.add(
            responses.POST,
            self.project_attributes_url,
            json=self.project_attributes_json[0],
            status=204,
        )
        project = self.tamr.projects.by_external_id(self.project_external_id)
        # project.attributes.create MUST make a POST request to self.project_attributes_url
        # If it posts to some other URL, responses will raise an exception;
        # If it does not post to any URL, responses will also raise an exception.
        project.attributes.create(self.project_attributes_json[0])

    def test_project_get_input_datasets(self):
        p = Project(self.tamr, self.project_json[0])
        datasets = p.input_datasets()
        self.assertEqual(datasets.api_path, "projects/1/inputDatasets")

    @responses.activate
    def test_return_attribute_collection(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        project = self.tamr.projects.by_external_id(self.project_external_id)
        attribute_configs = project.attribute_configurations()
        self.assertEqual(
            attribute_configs.api_path, "projects/1/attributeConfigurations"
        )

    @responses.activate
    def test_return_attribute_mapping(self):
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        map_url = "http://localhost:9100/api/versioned/v1/projects/1/attributeMappings"
        responses.add(responses.GET, map_url, json=self.mappings_json)
        project = self.tamr.projects.by_external_id(self.project_external_id)
        attribute_mappings = project.attribute_mappings()
        self.assertEqual(
            attribute_mappings.by_resource_id("19689-14").unified_dataset_name,
            self.mappings_json[0]["unifiedDatasetName"],
        )

    dataset_external_id = "1"
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets?filter=externalId=={dataset_external_id}"
    dataset_json = [
        {
            "id": "unify://unified-data/v1/datasets/1",
            "externalId": "1",
            "name": "dataset 1 name",
            "description": "dataset 1 description",
            "version": "dataset 1 version",
            "keyAttributeNames": ["tamr_id"],
            "tags": [],
            "created": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.636Z",
                "version": "dataset 1 created version",
            },
            "lastModified": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.851Z",
                "version": "dataset 1 modified version",
            },
            "relativeId": "datasets/1",
            "upstreamDatasetIds": [],
        }
    ]
    project_json = [
        {
            "id": "unify://unified-data/v1/projects/1",
            "externalId": "project 1 external ID",
            "name": "project 1 name",
            "description": "project 1 description",
            "type": "DEDUP",
            "unifiedDatasetName": "project 1 unified dataset",
            "created": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.636Z",
                "version": "project 1 created version",
            },
            "lastModified": {
                "username": "admin",
                "time": "2018-09-10T16:06:20.851Z",
                "version": "project 1 modified version",
            },
            "relativeId": "projects/1",
        }
    ]
    project_external_id = "project 1 external ID"
    projects_url = f"http://localhost:9100/api/versioned/v1/projects?filter=externalId=={project_external_id}"
    post_input_datasets_json = []
    input_datasets_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/inputDatasets"
    )
    get_input_datasets_json = dataset_json

    project_attributes_url = (
        "http://localhost:9100/api/versioned/v1/projects/1/attributes"
    )
    project_attributes_json = [
        {
            "name": "id",
            "description": "identifier",
            "type": {"baseType": "STRING"},
            "isNullable": False,
        },
        {
            "name": "name",
            "description": "full name",
            "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
            "isNullable": True,
        },
        {
            "name": "description",
            "description": "human readable description",
            "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
            "isNullable": True,
        },
    ]

    mappings_json = [
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19689-14",
            "relativeId": "projects/1/attributeMappings/19689-14",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/suburb",
            "relativeInputAttributeId": "datasets/6/attributes/suburb",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "suburb",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/suburb",
            "relativeUnifiedAttributeId": "datasets/8/attributes/suburb",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "suburb",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19690-7",
            "relativeId": "projects/1/attributeMappings/19690-7",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/sex",
            "relativeInputAttributeId": "datasets/6/attributes/sex",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "sex",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/sex",
            "relativeUnifiedAttributeId": "datasets/8/attributes/sex",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "sex",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19691-18",
            "relativeId": "projects/1/attributeMappings/19691-18",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_2",
            "relativeInputAttributeId": "datasets/6/attributes/address_2",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "address_2",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/address_2",
            "relativeUnifiedAttributeId": "datasets/8/attributes/address_2",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "address_2",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19692-8",
            "relativeId": "projects/1/attributeMappings/19692-8",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/age",
            "relativeInputAttributeId": "datasets/6/attributes/age",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "age",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/age",
            "relativeUnifiedAttributeId": "datasets/8/attributes/age",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "age",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19693-6",
            "relativeId": "projects/1/attributeMappings/19693-6",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/culture",
            "relativeInputAttributeId": "datasets/6/attributes/culture",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "culture",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/culture",
            "relativeUnifiedAttributeId": "datasets/8/attributes/culture",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "culture",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19694-16",
            "relativeId": "projects/1/attributeMappings/19694-16",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/street_number",
            "relativeInputAttributeId": "datasets/6/attributes/street_number",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "street_number",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/street_number",
            "relativeUnifiedAttributeId": "datasets/8/attributes/street_number",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "street_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19695-15",
            "relativeId": "projects/1/attributeMappings/19695-15",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/postcode",
            "relativeInputAttributeId": "datasets/6/attributes/postcode",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "postcode",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/postcode",
            "relativeUnifiedAttributeId": "datasets/8/attributes/postcode",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "postcode",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19696-19",
            "relativeId": "projects/1/attributeMappings/19696-19",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/phone_number",
            "relativeInputAttributeId": "datasets/6/attributes/phone_number",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "phone_number",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/phone_number",
            "relativeUnifiedAttributeId": "datasets/8/attributes/phone_number",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "phone_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19697-20",
            "relativeId": "projects/1/attributeMappings/19697-20",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/soc_sec_id",
            "relativeInputAttributeId": "datasets/6/attributes/soc_sec_id",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "soc_sec_id",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/soc_sec_id",
            "relativeUnifiedAttributeId": "datasets/8/attributes/soc_sec_id",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "soc_sec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19698-5",
            "relativeId": "projects/1/attributeMappings/19698-5",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/rec2_id",
            "relativeInputAttributeId": "datasets/6/attributes/rec2_id",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "rec2_id",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/rec2_id",
            "relativeUnifiedAttributeId": "datasets/8/attributes/rec2_id",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "rec2_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19699-9",
            "relativeId": "projects/1/attributeMappings/19699-9",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/date_of_birth",
            "relativeInputAttributeId": "datasets/6/attributes/date_of_birth",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "date_of_birth",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/date_of_birth",
            "relativeUnifiedAttributeId": "datasets/8/attributes/date_of_birth",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "date_of_birth",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19700-10",
            "relativeId": "projects/1/attributeMappings/19700-10",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/title",
            "relativeInputAttributeId": "datasets/6/attributes/title",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "title",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/title",
            "relativeUnifiedAttributeId": "datasets/8/attributes/title",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "title",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19701-17",
            "relativeId": "projects/1/attributeMappings/19701-17",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_1",
            "relativeInputAttributeId": "datasets/6/attributes/address_1",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "address_1",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/address_1",
            "relativeUnifiedAttributeId": "datasets/8/attributes/address_1",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "address_1",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19702-4",
            "relativeId": "projects/1/attributeMappings/19702-4",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/rec_id",
            "relativeInputAttributeId": "datasets/6/attributes/rec_id",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "rec_id",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/rec_id",
            "relativeUnifiedAttributeId": "datasets/8/attributes/rec_id",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "rec_id",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19703-13",
            "relativeId": "projects/1/attributeMappings/19703-13",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/state",
            "relativeInputAttributeId": "datasets/6/attributes/state",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "state",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/state",
            "relativeUnifiedAttributeId": "datasets/8/attributes/state",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "state",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19704-22",
            "relativeId": "projects/1/attributeMappings/19704-22",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/family_role",
            "relativeInputAttributeId": "datasets/6/attributes/family_role",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "family_role",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/family_role",
            "relativeUnifiedAttributeId": "datasets/8/attributes/family_role",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "family_role",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19705-21",
            "relativeId": "projects/1/attributeMappings/19705-21",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/blocking_number",
            "relativeInputAttributeId": "datasets/6/attributes/blocking_number",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "blocking_number",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/blocking_number",
            "relativeUnifiedAttributeId": "datasets/8/attributes/blocking_number",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "blocking_number",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19706-12",
            "relativeId": "projects/1/attributeMappings/19706-12",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/surname",
            "relativeInputAttributeId": "datasets/6/attributes/surname",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "surname",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/surname",
            "relativeUnifiedAttributeId": "datasets/8/attributes/surname",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "surname",
        },
        {
            "id": "unify://unified-data/v1/projects/1/attributeMappings/19707-11",
            "relativeId": "projects/1/attributeMappings/19707-11",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/given_name",
            "relativeInputAttributeId": "datasets/6/attributes/given_name",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "given_name",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/8/attributes/given_name",
            "relativeUnifiedAttributeId": "datasets/8/attributes/given_name",
            "unifiedDatasetName": "Project_1_unified_dataset",
            "unifiedAttributeName": "given_name",
        },
    ]
