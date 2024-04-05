user_filter_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "maxLength": 50},
        "email": {"format": "email"},
    },
    "optional": ["username", "email"]
}
