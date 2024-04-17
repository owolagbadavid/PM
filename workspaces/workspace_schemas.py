workspace_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
    },
    "required": ["name", "description"]
}

workspace_filter_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "page": {"type": "string", "format": "number"},
        "count": {"type": "string", "format": "number"}
    },
    "optional": ["name", "description", "page", "count"]
}
