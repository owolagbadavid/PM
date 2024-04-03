login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "maxLength": 50},
        "password": {"type": "string", "minLength": 6}
    },
    "required": ["username", "password"]
}


register_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "maxLength": 50},
        "email": {"format": "email"},
        "password": {"type": "string", "minLength": 6},
        "passwordConfirm": {"type": "string", "minLength": 6},
    },
    "required": ["username", "password", "passwordConfirm", "email"]
}
