AttributeType
=============

See https://docs.tamr.com/reference#attribute-types

.. autodata:: tamr_client.attribute.type.BOOLEAN
.. autodata:: tamr_client.attribute.type.DOUBLE
.. autodata:: tamr_client.attribute.type.INT
.. autodata:: tamr_client.attribute.type.LONG
.. autodata:: tamr_client.attribute.type.STRING

.. autodata:: tamr_client.attribute.type.DEFAULT
.. autodata:: tamr_client.attribute.type.GEOSPATIAL


.. NOTE(pcattori):
   `Array` has a recursive dependency on `AttributeType`.
   `sphinx_autodoc_typehint` cannot handle recursive dependencies,
   so reference docs are written manually

.. class:: tamr_client.attribute.type.Array(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`

.. NOTE(pcattori):
   `Map` has a recursive dependency on `AttributeType`.
   `sphinx_autodoc_typehint` cannot handle recursive dependencies,
   so reference docs are written manually

.. class:: tamr_client.attribute.type.Map(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`


.. autoclass:: tamr_client.attribute.type.Record

.. autofunction:: tamr_client.attribute.type.from_json
.. autofunction:: tamr_client.attribute.type.to_json
