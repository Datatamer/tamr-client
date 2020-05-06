from tamr_client.attributes.subattribute import SubAttribute
from tamr_client.attributes.attribute_type import Array, DOUBLE, Record, STRING

DEFAULT: Array = Array(STRING)

GEOSPATIAL: Record = Record(
    attributes=(
        SubAttribute(name="point", is_nullable=True, type=Array(DOUBLE)),
        SubAttribute(name="multiPoint", is_nullable=True, type=Array(Array(DOUBLE))),
        SubAttribute(name="lineString", is_nullable=True, type=Array(Array(DOUBLE))),
        SubAttribute(
            name="multiLineString", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        SubAttribute(
            name="polygon", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        SubAttribute(
            name="multiPolygon",
            is_nullable=True,
            type=Array(Array(Array(Array(DOUBLE)))),
        ),
    )
)
