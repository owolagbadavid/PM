workspace_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
    },
    "required": ["name", "description"]
}
