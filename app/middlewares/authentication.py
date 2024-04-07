from utils import verify_token
from flask import request, abort
from users.user_service import get_user_by_id


def authenticate_user():
    try:
        payload = verify_token(request.headers.get('Authorization', ""))
        user = get_user_by_id(payload['id'])
        if not user:
            raise Exception
        request.user = user
    except Exception as e:
        print(e)
        abort(401, 'Unauthorized')

# check if user owns has access to requested resource


def authorize_user(resouce, resource_id):
    if resouce == 'workspace':
        pass
