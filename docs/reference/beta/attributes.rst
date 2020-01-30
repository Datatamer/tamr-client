Attributes
==========

Attribute
---------

.. autoclass:: tamr_unify_client.Attribute

.. TODO(pcattori): note about import path
.. autofunction:: tamr_unify_client.attributes.attribute.from_resource_id
.. autofunction:: tamr_unify_client.attributes.attribute.to_json
.. autofunction:: tamr_unify_client.attributes.attribute.create
.. autofunction:: tamr_unify_client.attributes.attribute.update
.. autofunction:: tamr_unify_client.attributes.attribute.delete

AttributeType
-------------

.. autoclass:: tamr_unify_client.attribute_type.Boolean
.. autoclass:: tamr_unify_client.attribute_type.Double
.. autoclass:: tamr_unify_client.attribute_type.Int
.. autoclass:: tamr_unify_client.attribute_type.Long
.. autoclass:: tamr_unify_client.attribute_type.String

.. NOTE(pcattori): Manually write docs for complex attribute types
   Complex types recursively reference other attribute types or subattributes
   sphinx_autodoc_typehints cannot properly parse types recursively

.. class:: tamr_unify_client.attribute_type.Array(inner_type)

   See https://docs.tamr.com/reference#attribute-types
   
   :param inner_type:
   :type inner_type: :class:`~tamr_unify_client.AttributeType`

.. class:: tamr_unify_client.attribute_type.Map(inner_type)

   See https://docs.tamr.com/reference#attribute-types

   :param inner_type:
   :type inner_type: :class:`~tamr_unify_client.AttributeType`

.. class:: tamr_unify_client.attribute_type.Record(attributes)

   See https://docs.tamr.com/reference#attribute-types

   :param attributes:
   :type attributes: :class:`~typing.Tuple` [:class:`~tamr_unify_client.SubAttribute`]

.. autofunction:: tamr_unify_client.attribute_type.from_json
.. autofunction:: tamr_unify_client.attribute_type.to_json

SubAttribute
------------

.. autoclass:: tamr_unify_client.SubAttribute

.. autofunction:: tamr_unify_client.subattribute.from_json
.. autofunction:: tamr_unify_client.subattribute.to_json
