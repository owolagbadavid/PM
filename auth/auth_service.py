from .auth_schemas import login_schema, register_schema
from utils.validate_json import validate_json
from users.user_service import create_user, get_user_by_email
from utils import model_to_dict, sign_token
from werkzeug.exceptions import Unauthorized, UnprocessableEntity, HTTPException


def login_service(data):
    validate_json(data, login_schema)
    user = get_user_by_email(data['email'])
    if user and user.check_password_correction(data['password']):
        user_dict = model_to_dict(user)
        user_dict.pop('password_hash')
        return sign_token(user_dict)
    raise Unauthorized('Incorrect email or password')


def register_service(data):
    validate_json(data, register_schema)
    try:
        user = create_user(data)
    except Exception as e:
        print(e)
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Error creating account! Try again later')
    user_dict = model_to_dict(user)
    user_dict.pop('password_hash')
    return sign_token(user_dict)
