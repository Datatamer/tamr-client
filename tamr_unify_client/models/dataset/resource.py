import json

from tamr_unify_client.models.attribute.collection import AttributeCollection
from tamr_unify_client.models.base_resource import BaseResource
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
        :type records: list[dict]
        """
        body = "\n".join([json.dumps(r) for r in records])
        self.client.post(self.api_path + ":updateRecords", data=body)

    def refresh(self, **options):
        """Brings dataset up-to-date if needed, taking whatever actions are required.

        :param ``**options``: Options passed to underlying :class:`~tamr_unify_client.models.operation.Operation` .
            See :func:`~tamr_unify_client.models.operation.Operation.apply_options` .
        """
        op_json = self.client.post(self.api_path + ":refresh").successful().json()
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
            "features": [feature for feature in self.__geo_features__],
        }

    @property
    def __geo_features__(self):
        """A generator of the records in this dataset represented as geospatial features

        See https://gist.github.com/sgillies/2217756

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

        # Duck-typing: find all the attributes that look like geometry
        geo_attr_names = {
            "point",
            "multiPoint",
            "lineString",
            "multiLineString",
            "polygon",
            "multiPolygon",
        }
        geo_attrs = [
            attr.name
            for attr in self.attributes
            if "RECORD" == attr.type.base_type
            and geo_attr_names.intersection(
                {sub_attr.name for sub_attr in attr.type.attributes}
            )
        ]
        # We select the first such attribute as the geometry
        if geo_attrs:
            geo_attr = geo_attrs[0]
        else:
            geo_attr = None
        for record in self.records():
            yield self._record_to_feature(record, key_value, key_attrs, geo_attr)

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
        conversion = {
            "point": "Point",
            "multiPoint": "MultiPoint",
            "lineString": "LineString",
            "multiLineString": "MultiLineString",
            "polygon": "Polygon",
            "multiPolygon": "MultiPolygon",
        }
        if geo_attr in record:
            src_geo = record[geo_attr]
            for unify_attr in conversion.keys():
                if unify_attr in src_geo and src_geo[unify_attr]:
                    feature["geometry"] = {
                        "type": conversion[unify_attr],
                        "coordinates": src_geo[unify_attr],
                    }
                    break
        if "bbox" in record:
            feature["bbox"] = record["bbox"]
        non_reserved = set(record.keys()).difference(reserved)
        if non_reserved:
            feature["properties"] = {attr: record[attr] for attr in non_reserved}
        return feature

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r}, "
            f"version={self.version!r})"
        )
