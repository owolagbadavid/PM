user_filter_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string", "maxLength": 30},
        "last_name": {"type": "string", "maxLength": 30},
        "email": {"format": "email"},
        "page": {"type": "integer"},
        "count": {"type": "integer"}
    },
    "optional": ["first_name", "email", "last_name", "page", "count"]
}
