from copy import deepcopy
import json
import os
from typing import Optional, TYPE_CHECKING
import warnings

from tamr_unify_client._ignore_nan_encoder import IgnoreNanEncoder
from tamr_unify_client.attribute.collection import AttributeCollection
from tamr_unify_client.base_resource import BaseResource
from tamr_unify_client.dataset.profile import DatasetProfile
from tamr_unify_client.dataset.status import DatasetStatus
from tamr_unify_client.dataset.uri import DatasetURI
from tamr_unify_client.dataset.usage import DatasetUsage
from tamr_unify_client.operation import Operation

BUILDING_DOCS = os.environ.get("TAMR_CLIENT_DOCS") == "1"
if TYPE_CHECKING or BUILDING_DOCS:
    import pandas as pd


class Dataset(BaseResource):
    """A Tamr dataset."""

    @classmethod
    def from_json(cls, client, resource_json, api_path=None):
        return super().from_data(client, resource_json, api_path)

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    @property
    def external_id(self):
        """:type: str"""
        return self._data.get("externalId")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def version(self):
        """:type: str"""
        return self._data.get("version")

    @property
    def tags(self):
        """:type: list[str]"""
        return self._data.get("tags")[:]

    @property
    def key_attribute_names(self):
        """:type: list[str]"""
        return self._data.get("keyAttributeNames")[:]

    @property
    def attributes(self):
        """Attributes of this dataset.

        :return: Attributes of this dataset.
        :rtype: :class:`~tamr_unify_client.attribute.collection.AttributeCollection`
        """
        alias = self.api_path + "/attributes"
        return AttributeCollection(self.client, alias)

    def _update_records(self, updates, *, ignore_nan=False):
        """Send a batch of record creations/updates/deletions to this dataset.
        You probably want to use :func:`~tamr_unify_client.dataset.resource.Dataset.upsert_records`
        or :func:`~tamr_unify_client.dataset.resource.Dataset.delete_records` instead.

        :param records: Each record should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.
        :type records: iterable[dict]
        :param ignore_nan: Whether to treat `NaN` values as null. Unconverted `NaN`s will raise an error if found. Deprecated.
        :type ignore_nan: bool
        :returns: JSON response body from server.
        :rtype: :py:class:`dict`
        """
        if ignore_nan:
            warnings.warn(
                "'ignore_nan' is deprecated. Users are expected to provide valid JSON representations instead",
                DeprecationWarning,
            )
        encoder = IgnoreNanEncoder if ignore_nan else None
        stringified_updates = (
            json.dumps(update, cls=encoder, allow_nan=False).encode("utf-8")
            for update in updates
        )

        return (
            self.client.post(
                self.api_path + ":updateRecords",
                headers={"Content-Encoding": "utf-8"},
                data=stringified_updates,
            )
            .successful()
            .json()
        )

    def upsert_from_dataframe(
        self,
        df: "pd.DataFrame",
        *,
        primary_key_name: str,
        ignore_nan: Optional[bool] = None,
    ) -> dict:
        """Upserts a record for each row of `df` with attributes for each column in `df`.

        Args:
            df: The data to upsert records from.
            primary_key_name: The name of the primary key of the dataset.  Must be a column of `df`.
            ignore_nan: Legacy parameter that does nothing. Deprecated.

        Returns:
            JSON response body from the server.

        Raises:
            KeyError: If `primary_key_name` is not a column in `df`.

        """
        if ignore_nan is not None:
            warnings.warn(
                "'ignore_nan' is deprecated. DataFrame `NaN`s are always ignored in upsert",
                DeprecationWarning,
            )
        if primary_key_name not in df.columns:
            raise KeyError(f"{primary_key_name} is not an attribute of the data")

        # serialize records via to_json to handle `np.nan` values
        serialized_records = ((pk, row.to_json()) for pk, row in df.iterrows())
        records = (
            {primary_key_name: pk, **json.loads(row)} for pk, row in serialized_records
        )
        return self.upsert_records(records, primary_key_name)

    def upsert_records(self, records, primary_key_name, *, ignore_nan=False):
        """Creates or updates the specified records.

        :param records: The records to update, as dictionaries.
        :type records: iterable[dict]
        :param primary_key_name: The name of the primary key for these records, which must be a key in each record dictionary.
        :type primary_key_name: str
        :param ignore_nan: Whether to convert `NaN` values to `null` when upserting records.  If `False` and `NaN` is found this function will fail. Deprecated.
        :type ignore_nan: bool
        :return: JSON response body from the server.
        :rtype: dict
        """
        if ignore_nan:
            warnings.warn(
                "'ignore_nan' is deprecated. Users are expected to provide valid JSON representations instead",
                DeprecationWarning,
            )
        updates = (
            {"action": "CREATE", "recordId": record[primary_key_name], "record": record}
            for record in records
        )
        return self._update_records(updates, ignore_nan=ignore_nan)

    def delete_records(self, records, primary_key_name):
        """Deletes the specified records.

        :param records: The records to delete, as dictionaries.
        :type records: iterable[dict]
        :param primary_key_name: The name of the primary key for these records, which must be a key in each record dictionary.
        :type primary_key_name: str
        :return: JSON response body from the server.
        :rtype: dict
        """
        ids = (record[primary_key_name] for record in records)
        return self.delete_records_by_id(ids)

    def delete_records_by_id(self, record_ids):
        """Deletes the specified records.

        :param record_ids: The IDs of the records to delete.
        :type record_ids: iterable
        :return: JSON response body from the server.
        :rtype: dict
        """
        updates = ({"action": "DELETE", "recordId": rid} for rid in record_ids)
        return self._update_records(updates)

    def delete_all_records(self):
        """Removes all records from the dataset.

        :return: HTTP response from the server
        :rtype: :class:`requests.Response`
        """
        path = self.api_path + "/records"
        response = self.client.delete(path).successful()
        return response

    def refresh(self, **options):
        """Brings dataset up-to-date if needed, taking whatever actions are required.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.operation.Operation` .
            See :func:`~tamr_unify_client.operation.Operation.apply_options` .
        :returns: The refresh operation.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        response = self.client.post(self.api_path + ":refresh").successful()
        op = Operation.from_response(self.client, response)
        return op.apply_options(**options)

    def profile(self):
        """Returns profile information for a dataset.

        If profile information has not been generated, call create_profile() first.
        If the returned profile information is out-of-date, you can call refresh() on the returned
        object to bring it up-to-date.

        :return: Dataset Profile information.
        :rtype: :class:`~tamr_unify_client.dataset.profile.DatasetProfile`
        """
        profile_json = self.client.get(self.api_path + "/profile").successful().json()
        return DatasetProfile.from_json(
            self.client, profile_json, api_path=self.api_path + "/profile"
        )

    def create_profile(self, **options):
        """Create a profile for this dataset.

        If a profile already exists, the existing profile will be brought
        up to date.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.operation.Operation` .
            See :func:`~tamr_unify_client.operation.Operation.apply_options` .
        :return: The operation to create the profile.
        :rtype: :class:`~tamr_unify_client.operation.Operation`
        """
        response = self.client.post(self.api_path + "/profile:refresh").successful()
        op = Operation.from_response(self.client, response)
        return op.apply_options(**options)

    def records(self):
        """Stream this dataset's records as Python dictionaries.

        :return: Stream of records.
        :rtype: Python generator yielding :py:class:`dict`
        """
        with self.client.get(self.api_path + "/records", stream=True) as response:
            for line in response.iter_lines():
                yield json.loads(line)

    def status(self):
        """Retrieve this dataset's streamability status.

        :return: Dataset streamability status.
        :rtype: :class:`~tamr_unify_client.dataset.status.DatasetStatus`
        """
        status_json = self.client.get(self.api_path + "/status").successful().json()
        return DatasetStatus.from_json(
            self.client, status_json, api_path=self.api_path + "/status"
        )

    def usage(self):
        """Retrieve this dataset's usage by recipes and downstream datasets.

        :return: The dataset's usage.
        :rtype: :class:`~tamr_unify_client.dataset.usage.DatasetUsage`
        """
        alias = self.api_path + "/usage"
        usage = self.client.get(alias).successful().json()
        return DatasetUsage.from_json(self.client, usage, alias)

    def from_geo_features(self, features, geo_attr=None):
        """Upsert this dataset from a geospatial FeatureCollection or iterable of Features.

        `features` can be:

        - An object that implements ``__geo_interface__`` as a FeatureCollection
          (see https://gist.github.com/sgillies/2217756)
        - An iterable of features, where each element is a feature dictionary or an object
          that implements the ``__geo_interface__`` as a Feature
        - A map where the "features" key contains an iterable of features

        See: geopandas.GeoDataFrame.from_features()

        If geo_attr is provided, then the named Tamr attribute will be used for the geometry.
        If geo_attr is not provided, then the first attribute on the dataset with geometry type
        will be used for the geometry.

        :param features: geospatial features
        :param geo_attr: (optional) name of the Tamr attribute to use for the feature's geometry
        :type geo_attr: str
        :returns: JSON response body from server.
        :rtype: :py:class:`dict`
        """
        if hasattr(features, "__geo_interface__"):
            features = features.__geo_interface__
        if hasattr(features, "get") and features.get("type") == "FeatureCollection":
            features = features["features"]

        key_attrs = self.key_attribute_names
        if len(key_attrs) == 1:
            record_id = "recordId"
        else:
            record_id = "compositeRecordId"

        if geo_attr is None:
            geo_attr = self._geo_attr

        return self._update_records(
            self._features_to_updates(features, record_id, key_attrs, geo_attr)
        )

    def upstream_datasets(self):
        """The Dataset's upstream datasets.

        API returns the URIs of the upstream datasets,
        resulting in a list of DatasetURIs, not actual Datasets.

        :return: A list of the Dataset's upstream datasets.
        :rtype: list[:class:`~tamr_unify_client.dataset.uri.DatasetURI`]
        """
        alias = self.api_path + "/upstreamDatasets"
        resources = self.client.get(alias).successful().json()

        return [DatasetURI(self.client, uri) for uri in resources]

    def spec(self):
        """Returns this dataset's spec.

        :return: The spec of this dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return DatasetSpec.of(self)

    def delete(self, cascade=False):
        """Deletes this dataset, optionally deleting all derived datasets as well.

        :param cascade: Whether to delete all datasets derived from this one. Optional, default is `False`.
            Do not use this option unless you are certain you need it as it can have unindended consequences.
        :type cascade: bool
        :return: HTTP response from the server
        :rtype: :class:`requests.Response`
        """
        params = {"cascade": cascade}
        response = self.client.delete(self.api_path, params=params).successful()
        return response

    @property
    def __geo_interface__(self):
        """Retrieve a representation of this dataset that conforms to the Python Geo Interface.

        Note that this materializes all features; for a streaming interface to features,
        see :method:`~tamr_unify_client.dataset.Dataset.__geo_features__()`

        See https://gist.github.com/sgillies/2217756

        :return: dict[str, object]
        """
        return {
            "type": "FeatureCollection",
            "features": [feature for feature in self.itergeofeatures()],
        }

    def itergeofeatures(self, geo_attr=None):
        """Returns an iterator that yields feature dictionaries that comply with __geo_interface__

        See https://gist.github.com/sgillies/2217756

        :param geo_attr: (optional) name of the Tamr attribute to use for the feature's geometry
        :type geo_attr: str
        :return: stream of features
        :rtype: Python generator yielding :py:class:`dict[str, object]`
        """
        key_attrs = self.key_attribute_names
        if len(key_attrs) == 1:

            def key_value(rec):
                return rec[key_attrs[0]]

        else:

            def key_value(rec):
                return [rec[attr] for attr in key_attrs]

        if geo_attr is None:
            geo_attr = self._geo_attr

        for record in self.records():
            yield self._record_to_feature(record, key_value, key_attrs, geo_attr)

    @property
    def _geo_attr(self):
        """The name of the attribute that contains geometry

        :return: the name of the attribute that contains geometry
        :rtype: str
        """
        # Duck-typing: find all the attributes that look like geometry
        geo_attrs = [
            attr.name
            for attr in self.attributes
            if "RECORD" == attr.type.base_type
            and self._geo_attr_names().intersection(
                {sub_attr.name for sub_attr in attr.type.attributes}
            )
        ]
        # We select the first such attribute as the geometry
        if geo_attrs:
            geo_attr = geo_attrs[0]
        else:
            geo_attr = None
        return geo_attr

    @staticmethod
    def _record_to_feature(record, key_value, key_attrs, geo_attr):
        """Convert a Tamr record to a Python Geo Interface Feature

        :param record: Tamr record
        :param key_value: Function to extract the value of the primary key from the record
        :param key_attrs: Set of attributes that comprise the primary key for the record
        :param geo_attr: The singular attribute to use as the geometry
        :return: map from str to object
        """
        feature = {"type": "Feature", "id": key_value(record)}
        reserved = {"bbox", geo_attr}.union(key_attrs)
        if geo_attr and geo_attr in record:
            src_geo = record[geo_attr]
            if src_geo:
                for unify_attr in Dataset._geo_attr_names():
                    if unify_attr in src_geo and src_geo[unify_attr]:
                        feature["geometry"] = {
                            # Convert e.g. multiLineString -> MultiLineString
                            "type": unify_attr[0].upper() + unify_attr[1:],
                            "coordinates": src_geo[unify_attr],
                        }
                        break
                    else:
                        feature["geometry"] = None
            else:
                feature["geometry"] = None
        if "bbox" in record:
            feature["bbox"] = record["bbox"]
        non_reserved = set(record.keys()).difference(reserved)
        if non_reserved:
            feature["properties"] = {attr: record[attr] for attr in non_reserved}
        return feature

    @staticmethod
    def _feature_to_record(feature, key_attrs, geo_attr):
        """Convert a Python Geo Interface Feature to a Tamr record

        feature can be a dict representing a Geospatial Feature, or a Feature object
        that implements the __geo_interface__ property.

        :param feature: Python Geo Interface Feature
        :param key_attrs: Sequence of attributes that comprise the primary key for the record
        :param geo_attr: The singluar attribute on the record to use for the geometry
        :return: dict
        """

        if hasattr(feature, "__geo_interface__"):
            feature = feature.__geo_interface__

        record = {}

        props = feature.get("properties")
        if props:
            for prop in props:
                record[prop] = props[prop]

        geometry = feature.get("geometry")
        if geometry:
            geo_type = geometry["type"]
            # Convert e.g. "MultiLineString" -> "multiLineString"
            geo_type = geo_type[0].lower() + geo_type[1:]
            record[geo_attr] = {geo_type: geometry["coordinates"]}

        bbox = feature.get("bbox")
        if bbox:
            record["bbox"] = bbox
        if "id" not in feature or feature["id"] is None:
            raise ValueError("id must have a non-null value")
        if key_attrs[1:]:
            key_values = feature["id"]

            for i, attr in enumerate(key_attrs):
                record[attr] = key_values[i]
        else:
            record[key_attrs[0]] = feature["id"]
        return record

    @staticmethod
    def _features_to_updates(features, id_attr, key_attrs, geo_attr):
        for feature in features:
            yield {
                "action": "CREATE",
                id_attr: feature["id"],
                "record": Dataset._feature_to_record(feature, key_attrs, geo_attr),
            }

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r}, "
            f"version={self.version!r})"
        )

    @staticmethod
    def _geo_attr_names():
        return {
            "point",
            "multiPoint",
            "lineString",
            "multiLineString",
            "polygon",
            "multiPolygon",
        }


class DatasetSpec:
    """A representation of the server view of a dataset."""

    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates a dataset spec from a dataset.

        :param resource: The existing dataset.
        :type resource: :class:`~tamr_unify_client.dataset.resource.Dataset`
        :return: The corresponding dataset spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return DatasetSpec(resource.client, deepcopy(resource._data), resource.api_path)

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new dataset.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return DatasetSpec(None, {}, None)

    def from_data(self, data):
        """Creates a spec with the same client and API path as this one, but new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return DatasetSpec(self.client, data, self.api_path)

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_name(self, new_name):
        """Creates a new spec with the same properties, updating name.

        :param new_name: The new name.
        :type new_name: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return self.from_data({**self._data, "name": new_name})

    def with_external_id(self, new_external_id):
        """Creates a new spec with the same properties, updating external ID.

        :param new_external_id: The new external ID.
        :type new_external_id: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return self.from_data({**self._data, "externalId": new_external_id})

    def with_description(self, new_description):
        """Creates a new spec with the same properties, updating description.

        :param new_description: The new description.
        :type new_description: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return self.from_data({**self._data, "description": new_description})

    def with_key_attribute_names(self, new_key_attribute_names):
        """Creates a new spec with the same properties, updating key attribute names.

       :param new_key_attribute_names: The new key attribute names.
       :type new_key_attribute_names: list[str]
       :return: A new spec.
       :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
       """
        return self.from_data(
            {**self._data, "keyAttributeNames": new_key_attribute_names}
        )

    def with_tags(self, new_tags):
        """Creates a new spec with the same properties, updating tags.

        :param new_tags: The new tags.
        :type new_tags: list[str]
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.dataset.resource.DatasetSpec`
        """
        return self.from_data({**self._data, "tags": new_tags})

    def put(self):
        """Updates the dataset on the server.

        :return: The modified dataset.
        :rtype: :class:`~tamr_unify_client.dataset.resource.Dataset`
        """
        new_data = self.client.put(self.api_path, json=self._data).successful().json()
        return Dataset.from_json(self.client, new_data, self.api_path)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )
