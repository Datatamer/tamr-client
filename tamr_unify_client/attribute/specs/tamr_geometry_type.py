TAMR_GEOMETRY_TYPE = {
    "name": None,
    "description": "",
    "type": {
        "baseType": "RECORD",
        "attributes": [
            {
                "name": "point",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "DOUBLE",
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
            {
                "name": "multiPoint",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "ARRAY",
                        "innerType": {
                            "baseType": "DOUBLE",
                            "attributes": [],
                        },
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
            {
                "name": "lineString",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "ARRAY",
                        "innerType": {
                            "baseType": "DOUBLE",
                            "attributes": [],
                        },
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
            {
                "name": "multiLineString",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "ARRAY",
                        "innerType": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "DOUBLE",
                                "attributes": [],
                            },
                            "attributes": [],
                        },
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
            {
                "name": "polygon",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "ARRAY",
                        "innerType": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "DOUBLE",
                                "attributes": [],
                            },
                            "attributes": [],
                        },
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
            {
                "name": "multiPolygon",
                "type": {
                    "baseType": "ARRAY",
                    "innerType": {
                        "baseType": "ARRAY",
                        "innerType": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "ARRAY",
                                "innerType": {
                                    "baseType": "DOUBLE",
                                    "attributes": [],
                                },
                                "attributes": [],
                            },
                            "attributes": [],
                        },
                        "attributes": [],
                    },
                    "attributes": [],
                },
                "isNullable": True,
            },
        ],
    },
    "isNullable": False,
}
