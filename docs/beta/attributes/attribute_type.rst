AttributeType
=============

See https://docs.tamr.com/reference#attribute-types

.. autodata:: tamr_client.attribute_type.BOOLEAN
.. autodata:: tamr_client.attribute_type.DOUBLE
.. autodata:: tamr_client.attribute_type.INT
.. autodata:: tamr_client.attribute_type.LONG
.. autodata:: tamr_client.attribute_type.STRING

.. NOTE(pcattori): Manually write docs for complex attribute types
   Complex types recursively reference other attribute types or subattributes
   sphinx_autodoc_typehints cannot properly parse types recursively

.. class:: tamr_client.attribute_type.Array(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`

.. class:: tamr_client.attribute_type.Map(inner_type)

   :param inner_type:
   :type inner_type: :class:`~tamr_client.AttributeType`

.. class:: tamr_client.attribute_type.Record(attributes)

  :param attributes:
  :type attributes: :class:`~typing.Tuple` [:class:`~tamr_client.SubAttribute`]

.. autofunction:: tamr_client.attribute_type.from_json
.. autofunction:: tamr_client.attribute_type.to_json

Type aliases
------------

.. autodata:: tamr_client.attribute_type_alias.DEFAULT
.. autodata:: tamr_client.attribute_type_alias.GEOSPATIAL
