AttributeType
=============

See https://docs.tamr.com/reference#attribute-types

.. autodata:: tamr_client.attributes.type.BOOLEAN
.. autodata:: tamr_client.attributes.type.DOUBLE
.. autodata:: tamr_client.attributes.type.INT
.. autodata:: tamr_client.attributes.type.LONG
.. autodata:: tamr_client.attributes.type.STRING

.. autodata:: tamr_client.attributes.type.DEFAULT
.. autodata:: tamr_client.attributes.type.GEOSPATIAL


.. NOTE(pcattori):
   `Array` has a recursive dependency on `AttributeType`.
   `sphinx_autodoc_typehint` cannot handle recursive dependencies,
   so reference docs are written manually

.. class:: tamr_client.attributes.type.Array(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`

.. NOTE(pcattori):
   `Map` has a recursive dependency on `AttributeType`.
   `sphinx_autodoc_typehint` cannot handle recursive dependencies,
   so reference docs are written manually

.. class:: tamr_client.attributes.type.Map(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`


.. autoclass:: tamr_client.attributes.type.Record

.. autofunction:: tamr_client.attributes.type.from_json
.. autofunction:: tamr_client.attributes.type.to_json
