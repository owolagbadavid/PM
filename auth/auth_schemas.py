login_schema = {
    "type": "object",
    "properties": {
        "email": {"format": "email"},  # "email": "string" is also valid
        "password": {"type": "string", "minLength": 6}
    },
    "required": ["email", "password"]
}


register_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string", "maxLength": 30},
        "last_name": {"type": "string", "maxLength": 30},
        "email": {"format": "email"},
        "password": {"type": "string", "minLength": 6},
    },
    "required": ["first_name", "last_name", "password", "email"]
}
