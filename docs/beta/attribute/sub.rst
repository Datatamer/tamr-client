SubAttribute
============

.. NOTE(pcattori):
   `SubAttribute` has a recursive dependency on `AttributeType`.
   `sphinx_autodoc_typehint` cannot handle recursive dependencies,
   so reference docs are written manually

.. class:: tamr_client.SubAttribute(name, type, is_nullable, description=None)

  :param name:
  :type name: :class:`str`
  :param type:
  :type type: :class:`~tamr_client.AttributeType`
  :param is_nullable:
  :type is_nullable: :class:`bool`
  :param description:
  :type description: :class:`~typing.Optional` [:class:`str`]

.. autofunction:: tamr_client.attribute.sub.from_json
.. autofunction:: tamr_client.attribute.sub.to_json
