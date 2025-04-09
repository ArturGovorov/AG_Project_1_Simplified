USER_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "email": {
            "type": "string",
        },
        "first_name": {
            "type": "string",
        },
        "last_name": {
            "type": "string",
        },
        "avatar": {
            "type": "string",
        },
    },
    "required": ["id", "email", "first_name", "last_name", "avatar"]
}

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
