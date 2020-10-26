import warnings

from requests.exceptions import HTTPError

from tamr_unify_client.base_collection import BaseCollection
from tamr_unify_client.dataset.resource import Dataset


class DatasetCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.dataset.resource.Dataset` s.

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path used to access this collection.
        E.g. ``"projects/1/inputDatasets"``.
        Default: ``"datasets"``.
    :type api_path: str
    """

    def __init__(self, client, api_path="datasets"):
        super().__init__(client, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve a dataset by resource ID.

        :param resource_id: The resource ID. E.g. ``"1"``
        :type resource_id: str
        :returns: The specified dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        return super().by_resource_id("datasets", resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve a dataset by relative ID.

        :param relative_id: The resource ID. E.g. ``"datasets/1"``
        :type relative_id: str
        :returns: The specified dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        return super().by_relative_id(Dataset, relative_id)

    def by_external_id(self, external_id):
        """Retrieve a dataset by external ID.

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified dataset, if found.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :raises KeyError: If no dataset with the specified external_id is found
        :raises LookupError: If multiple datasets with the specified external_id are found
        """
        return super().by_external_id(Dataset, external_id)

    def stream(self):
        """Stream datasets in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of datasets.
        :rtype: Python generator yielding :class:`~tamr_unify_client.dataset.resource.Dataset`

        Usage:
            >>> for dataset in collection.stream(): # explicit
            >>>     do_stuff(dataset)
            >>> for dataset in collection: # implicit
            >>>     do_stuff(dataset)
        """
        return super().stream(Dataset)

    def by_name(self, dataset_name):
        """Lookup a specific dataset in this collection by exact-match on name.

        :param dataset_name: Name of the desired dataset.
        :type dataset_name: str
        :return: Dataset with matching name in this collection.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :raises KeyError: If no dataset with specified name was found.
        """
        for dataset in self:
            if dataset.name == dataset_name:
                return dataset
        raise KeyError(f"No dataset found with name: {dataset_name}")

    def delete_by_resource_id(self, resource_id, cascade=False):
        """Deletes a dataset from this collection by resource_id. Optionally deletes all derived datasets as well.

        :param resource_id: The resource id of the dataset in this collection to delete.
        :type resource_id: str
        :param cascade: Whether to delete all datasets derived from the deleted one. Optional, default is `False`.
            Do not use this option unless you are certain you need it as it can have unindended consequences.
        :type cascade: bool
        :return: HTTP response from the server.
        :rtype: :class:`requests.Response`
        """
        params = {"cascade": cascade}
        path = f"{self.api_path}/{resource_id}"
        response = self.client.delete(path, params=params).successful()
        return response

    def create(self, creation_spec):
        """
        Create a Dataset in Tamr

        :param creation_spec: Dataset creation specification should be formatted as specified in the `Public Docs for Creating a Dataset <https://docs.tamr.com/reference#create-a-dataset>`_.
        :type creation_spec: dict[str, str]
        :returns: The created Dataset
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        return Dataset.from_json(self.client, data)

    def create_from_dataframe(
        self, df, primary_key_name, dataset_name, ignore_nan=None
    ):
        """Creates a dataset in this collection with the given name, creates an attribute for each column in the `df`
        (with `primary_key_name` as the key attribute), and upserts a record for each row of `df`.

        Each attribute has the default type `ARRAY[STRING]`, besides the key attribute, which will have type `STRING`.

        This function attempts to ensure atomicity, but it is not guaranteed. If an error occurs while creating
        attributes or records, an attempt will be made to delete the dataset that was created. However, if this
        request errors, it will not try again.

        :param df: The data to create the dataset with.
        :type df: :class:`pandas.DataFrame`
        :param primary_key_name: The name of the primary key of the dataset. Must be a column of `df`.
        :type primary_key_name: str
        :param dataset_name: What to name the dataset in Tamr. There cannot already be a dataset with this name.
        :type dataset_name: str
        :param ignore_nan: Legacy parameter that does nothing
        :type ignore_nan: bool
        :returns: The newly created dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :raises KeyError: If `primary_key_name` is not a column in `df`.
        :raises CreationError: If a step in creating the dataset fails.
        """
        if ignore_nan is not None:
            warnings.warn(
                "'ignore_nan' is deprecated. DataFrame `NaN`s are always ignored in upsert",
                DeprecationWarning,
            )
        if primary_key_name not in df.columns:
            raise KeyError(f"{primary_key_name} is not an attribute of the data")

        creation_spec = {"name": dataset_name, "keyAttributeNames": [primary_key_name]}
        try:
            dataset = self.create(creation_spec)
        except HTTPError:
            raise CreationError("Dataset was not created")
        # after this point, if a request fails, try to undo the change by deleting this dataset

        attributes = dataset.attributes
        for col in df.columns:
            if col == primary_key_name:
                # this attribute already exists, so don't create it again
                continue

            attr_spec = {
                "name": col,
                "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
            }
            try:
                attributes.create(attr_spec)
            except HTTPError:
                self._handle_creation_failure(dataset, "An attribute was not created")

        try:
            response = dataset.upsert_from_dataframe(
                df, primary_key_name=primary_key_name
            )
        except HTTPError:
            self._handle_creation_failure(dataset, "Records could not be created")

        if not response["allCommandsSucceeded"]:
            self._handle_creation_failure(dataset, "Some records had validation errors")

        return dataset

    def _handle_creation_failure(self, dataset, error):
        """Attempts to make create_from_dataframe atomic by deleting the created dataset in the event of later failure.
        However, this does not guarantee atomicity: if the request to delete the dataset fails, it will not retry.

        :param dataset: The created dataset to delete.
        :type dataset: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :param error: The error that caused the function to fail.
        :type error: str
        """
        try:
            dataset.delete()
        except HTTPError:
            raise CreationError("Created dataset didn't delete after an earlier error")
        raise CreationError(error)

    # super.__repr__ is sufficient


class CreationError(Exception):
    """An error from :func:`~tamr_unify_client.dataset.collection.DatasetCollection.create_from_dataframe`"""

    def __init__(self, error_message):
        super().__init__(error_message)
