Attributes
==========

Attribute
---------

.. autoclass:: tamr_client.Attribute

.. autofunction:: tamr_client.attribute.from_resource_id
.. autofunction:: tamr_client.attribute.to_json
.. autofunction:: tamr_client.attribute.create
.. autofunction:: tamr_client.attribute.update
.. autofunction:: tamr_client.attribute.delete

Exceptions
^^^^^^^^^^

.. autoclass:: tamr_client.ReservedAttributeName
  :no-inherited-members:

.. autoclass:: tamr_client.AttributeExists
  :no-inherited-members:

.. autoclass:: tamr_client.AttributeNotFound
  :no-inherited-members:

AttributeType
-------------

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
^^^^^^^^^^^^

.. autodata:: tamr_client.attribute_type_alias.DEFAULT
.. autodata:: tamr_client.attribute_type_alias.GEOSPATIAL

SubAttribute
------------

.. class:: tamr_client.SubAttribute(name, type, is_nullable, description=None)

  :param name:
  :type name: :class:`str`
  :param type:
  :type type: :class:`~tamr_client.AttributeType`
  :param is_nullable:
  :type is_nullable: :class:`bool`
  :param description:
  :type description: :class:`~typing.Optional` [:class:`str`]

.. autofunction:: tamr_client.subattribute.from_json
.. autofunction:: tamr_client.subattribute.to_json
