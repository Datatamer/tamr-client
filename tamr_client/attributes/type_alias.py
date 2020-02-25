import tamr_client as tc
from tamr_client.attributes.attribute_type import Array, DOUBLE, Record, STRING

DEFAULT: Array = Array(STRING)

GEOSPATIAL: Record = Record(
    attributes=(
        tc.SubAttribute(name="point", is_nullable=True, type=Array(DOUBLE)),
        tc.SubAttribute(name="multiPoint", is_nullable=True, type=Array(Array(DOUBLE))),
        tc.SubAttribute(name="lineString", is_nullable=True, type=Array(Array(DOUBLE))),
        tc.SubAttribute(
            name="multiLineString", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        tc.SubAttribute(
            name="polygon", is_nullable=True, type=Array(Array(Array(DOUBLE)))
        ),
        tc.SubAttribute(
            name="multiPolygon",
            is_nullable=True,
            type=Array(Array(Array(Array(DOUBLE)))),
        ),
    )
)
