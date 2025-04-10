LIST_RESOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
        "year": {
            "type": "integer",
        },
        "color": {
            "type": "string",
        },
        "pantone_value": {
            "type": "string",
        },
    },
    "required": ["id", "name", "year", "color", "pantone_value"]
}