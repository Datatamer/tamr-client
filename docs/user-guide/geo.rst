Geospatial Data
===============

What geospatial data is supported?
----------------------------------

In general, the Python Geo Interface is supported; see https://gist.github.com/sgillies/2217756

There are three layers of information:

- The outermost layer is a FeatureCollection
- Within a FeatureCollection are Features. Each feature has a type, an id, an optional
  geometry, an optional bbox (bounding box), and optional properties.
- A geometry has a type and coordinates.

Although the Python Geo Interface is non-prescriptive when it comes to the data types of
properties, Unify has a more restricted set of supported types. See https://docs.tamr.com/reference#attribute-types

Unify allows any number of geometry attributes per record; the Python Geo Interface is limited to
one. When converting Unify records to Python Geo Features, the first geometry attribute will
be used as the geometry; all other geometry attributes will appear as properties.

The :class:`~tamr_unify_client.models.dataset.resource.Dataset` class supports the
``__geo_interface__`` property. This will produce one ``FeatureCollection`` for the entire dataset.

There is a companion iterator ``iterfeatures()`` that returns a generator that allows you to
stream the records in the dataset as Geospatial features.

To produce a GeoJSON representation of a dataset::

  dataset = client.datasets.by_name("my_dataset")
  with open("my_dataset.json", "w") as f:
    json.dump(dataset.__geo_interface__, f)

Rules for converting between Unify records and Geospatial Features
------------------------------------------------------------------

The record's primary key will be used as the feature's ``id``. If the primary key is a single
attribute, then the value of that attribute will be the value of ``id``. If the primary key is
composed of multiple attributes, then the value of the ``id`` will be an array with the values
of the key attributes in order.

The first attribute with type ``RECORD`` containing an attribute named
``point``, ``multiPoint``, ``lineString``, ``multiLineString``, ``polygon``, or ``multiPolygon``
will be used as the geometry. No conversion is done between the coordinates as
represented in Unify and the coordinates in the feature.

If an attribute named ``bbox`` is available, it will be used as ``bbox``. No conversion is done
on the value of ``bbox``.

All other attributes will be placed in ``properties``, with no type conversion.

Streaming data access
---------------------

The ``Dataset`` method ``iterfeatures()`` returns a generator that allows you to
stream the records in the dataset as Geospatial features::

  dataset = client.datasets.by_name("my_dataset")
  for feature in dataset.iterfeatures():
    do_something(feature)

