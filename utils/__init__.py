import jwt


def model_to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}


def sign_token(payload):
    return jwt.encode(payload, 'secret', )


def verify_token(token):
    return jwt.decode(token, 'secret', "HS256")
