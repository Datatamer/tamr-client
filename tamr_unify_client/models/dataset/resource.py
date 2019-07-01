import json

from tamr_unify_client.models.attribute.collection import AttributeCollection
from tamr_unify_client.models.base_resource import BaseResource
from tamr_unify_client.models.dataset_profile import DatasetProfile
from tamr_unify_client.models.dataset_status import DatasetStatus
from tamr_unify_client.models.operation import Operation


class Dataset(BaseResource):
    """A Unify dataset."""

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
        return self._data.get("tags")

    @property
    def key_attribute_names(self):
        """:type: list[str]"""
        return self._data.get("keyAttributeNames")

    @property
    def attributes(self):
        """Attributes of this dataset.

        :return: Attributes of this dataset.
        :rtype: :class:`~tamr_unify_client.models.attribute.collection.AttributeCollection`
        """
        alias = self.api_path + "/attributes"
        resource_json = self.client.get(alias).successful().json()
        return AttributeCollection.from_json(self.client, resource_json, alias)

    def update_records(self, records):
        """Send a batch of record creations/updates/deletions to this dataset.

        :param records: Each record should be formatted as specified in the `Public Docs for Dataset updates <https://docs.tamr.com/reference#modify-a-datasets-records>`_.
        :type records: iterable[dict]
        :returns: JSON response body from server.
        :rtype: :py:class:`dict`
        """

        def _stringify_updates(updates):
            for update in updates:
                yield json.dumps(update).encode("utf-8")

        return (
            self.client.post(
                self.api_path + ":updateRecords",
                headers={"Content-Encoding": "utf-8"},
                data=_stringify_updates(records),
            )
            .successful()
            .json()
        )

    def refresh(self, **options):
        """Brings dataset up-to-date if needed, taking whatever actions are required.
        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        """
        op_json = self.client.post(self.api_path + ":refresh").successful().json()
        op = Operation.from_json(self.client, op_json)
        return op.apply_options(**options)

    def profile(self):
        """Returns profile information for a dataset.

        If profile information has not been generated, call create_profile() first.
        If the returned profile information is out-of-date, you can call refresh() on the returned
        object to bring it up-to-date.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
        :return: Dataset Profile information.
        :rtype: :class:`~tamr_unify_client.models.dataset_status.DatasetProfile`
        """
        profile_json = self.client.get(self.api_path + "/profile").successful().json()
        return DatasetProfile.from_json(
            self.client, profile_json, api_path=self.api_path + "/profile"
        )

    def create_profile(self, **options):
        """Create a profile for this dataset.

        If a profile already exists, the existing profile will be brought
        up to date.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        :return: the operation to create the profile.
        """
        op_json = (
            self.client.post(self.api_path + "/profile:refresh").successful().json()
        )
        op = Operation.from_json(self.client, op_json)
        return op.apply_options(**options)

    def records(self):
        """Stream this dataset's records as Python dictionaries.

        :return: Stream of records.
        :rtype: Python generator yielding :py:class:`dict`
        """
        with self.client.get(self.api_path + "/records", stream=True) as response:
            for line in response.iter_lines():
                yield json.loads(line)

    def status(self) -> DatasetStatus:
        """Retrieve this dataset's streamability status.

        :return: Dataset streamability status.
        :rtype: :class:`~tamr_unify_client.models.dataset_status.DatasetStatus`
        """
        status_json = self.client.get(self.api_path + "/status").successful().json()
        return DatasetStatus.from_json(
            self.client, status_json, api_path=self.api_path + "/status"
        )

    def from_geo_features(self, features, geo_attr=None):
        """Upsert this dataset from a geospatial FeatureCollection or iterable of Features.

        `features` can be:

        - An object that implements ``__geo_interface__`` as a FeatureCollection
          (see https://gist.github.com/sgillies/2217756)
        - An iterable of features, where each element is a feature dictionary or an object
          that implements the ``__geo_interface__`` as a Feature
        - A map where the "features" key contains an iterable of features

        See: geopandas.GeoDataFrame.from_features()

        If geo_attr is provided, then the named Unify attribute will be used for the geometry.
        If geo_attr is not provided, then the first attribute on the dataset with geometry type
        will be used for the geometry.

        :param features: geospatial features
        :param geo_attr: (optional) name of the Unify attribute to use for the feature's geometry
        :type geo_attr: str
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

        self.update_records(
            self._features_to_updates(features, record_id, key_attrs, geo_attr)
        )

    @property
    def __geo_interface__(self):
        """Retrieve a representation of this dataset that conforms to the Python Geo Interface.

        Note that this materializes all features; for a streaming interface to features,
        see :method:`~tamr_unify_client.models.dataset.Dataset.__geo_features__()`

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

        :param geo_attr: (optional) name of the Unify attribute to use for the feature's geometry
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
        """Convert a Unify record to a Python Geo Interface Feature

        :param record: Unify record
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
        """Convert a Python Geo Interface Feature to a Unify record

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
