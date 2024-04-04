project_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "maxLength": 30},
        "description": {"type": "string", "maxLength": 100},
        "start_date": {"type": "string", "format": "date-time"},
        "end_date": {"type": "string", "format": "date-time"},
        "workspace_id": {"type": "integer"}
    },
    "required": ["name", "description", "start_date", "end_date", "workspace_id"]
}
