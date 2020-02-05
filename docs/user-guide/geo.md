# Geospatial Data
## What geospatial data is supported?
In general, the Python Geo Interface is supported; see https://gist.github.com/sgillies/2217756

There are three layers of information, modeled after GeoJSON; see https://tools.ietf.org/html/rfc7946

* The outermost layer is a FeatureCollection
* Within a FeatureCollection are Features, each of which represents one "thing", like a building or a river. Each feature has:
  * type (string; required)
  * id (object; required)
  * geometry (Geometry, see below; optional)
  * bbox ("bounding box", 4 doubles; optional)
  * properties (map[string, object]; optional)
* Within a Feature is a Geometry, which represents a shape, like a point or a polygon. Each geometry has:
  * type (one of "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"; required)
  * coordinates (doubles; exactly how these are structured depends on the type of the geometry)

Although the Python Geo Interface is non-prescriptive when it comes to the data types of the id and properties, Tamr has a more restricted set of supported types. See https://docs.tamr.com/reference#attribute-types

The `:class:~tamr_unify_client.models.dataset.resource.Dataset` class supports the `__geo_interface__` property. This will produce one `FeatureCollection` for the entire dataset.

There is a companion iterator `itergeofeatures()` that returns a generator that allows you to
stream the records in the dataset as Geospatial features.

To produce a GeoJSON representation of a dataset:
```python
dataset = client.datasets.by_name("my_dataset")
with open("my_dataset.json", "w") as f:
    json.dump(dataset.__geo_interface__, f)
```

By default, `itergeofeatures()` will use the first dataset attribute with geometry type to fill in the feature geometry. You can override this by specifying the geometry attribute to use in the `geo_attr` parameter to `itergeofeatures`.

`Dataset` can also be updated from a feature collection that supports the Python Geo Interface:
```python
import geopandas
geodataframe = geopandas.GeoDataFrame(...)
dataset = client.dataset.by_name("my_dataset")
dataset.from_geo_features(geodataframe)
```

By default the features' geometries will be placed into the first dataset attribute with geometry
type. You can override this by specifying the geometry attribute to use in the `geo_attr`
parameter to `from_geo_features`.

## Rules for converting from Tamr records to Geospatial Features
The record's primary key will be used as the feature's `id`. If the primary key is a single attribute, then the value of that attribute will be the value of `id`. If the primary key is composed of multiple attributes, then the value of the `id` will be an array with the values of the key attributes in order.

Tamr allows any number of geometry attributes per record; the Python Geo Interface is limited to one. When converting Tamr records to Python Geo Features, the first geometry attribute in the schema will be used as the geometry; all other geometry attributes will appear as properties with no type conversion. In the future, additional control over the handling of multiple geometries may be provided; the current set of capabilities is intended primarily to support the use case of working with FeatureCollections within Tamr, and FeatureCollection has only one geometry per feature.

An attribute is considered to have geometry type if it has type `RECORD` and contains an attribute named `point`, `multiPoint`, `lineString`, `multiLineString`, `polygon`, or `multiPolygon`.

If an attribute named `bbox` is available, it will be used as `bbox`. No conversion is done on the value of `bbox`. In the future, additional control over the handling of `bbox` attributes may be provided.

All other attributes will be placed in `properties`, with no type conversion. This includes all geometry attributes other than the first.

## Rules for converting from Geospatial Features to Tamr records
The Feature's `id` will be converted into the primary key for the record. If the record uses a simple key, no value translation will be done. If the record uses a composite key, then the value of the Feature's `id` must be an array of values, one per attribute in the key.

If the Feature contains keys in `properties` that conflict with the record keys, `bbox`, or geometry, those keys are ignored (omitted).

If the Feature contains a `bbox`, it is copied to the record's `bbox`.

All other keys in the Feature's `properties` are propagated to the same-name attribute on the record, with no type conversion.

## Streaming data access
The `Dataset` method `itergeofeatures()` returns a generator that allows you to stream the records in the dataset as Geospatial features:
```python
my_dataset = client.datasets.by_name("my_dataset")
for feature in my_dataset.itergeofeatures():
    do_something(feature)
```

Note that many packages that consume the Python Geo Interface will be able to consume this
iterator directly. For example::
```python
from geopandas import GeoDataFrame
df = GeoDataFrame.from_features(my_dataset.itergeofeatures())
```
This allows construction of a GeoDataFrame directly from the stream of records, without materializing the intermediate dataset.
