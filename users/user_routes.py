from flask import Blueprint, request, jsonify, abort
from utils import verify_token, model_to_dict
from .user_controller import get_user_by_id
from werkzeug.exceptions import Unauthorized, NotFound


user_routes = Blueprint('user_routes', __name__)


@user_routes.before_request
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


@user_routes.errorhandler(Unauthorized)
def handle_unauthorized(error):
    response = jsonify(error=str(error))
    response.status_code = error.code
    return response


@user_routes.errorhandler(NotFound)
def handle_notfound(error):
    response = jsonify(error=str(error))
    response.status_code = error.code
    return response


@user_routes.route('me')
def get_me():
    user_dict = model_to_dict(request.user)
    user_dict.pop('password_hash')
    return jsonify(msg='User fetched successfully', user=user_dict), 200


@user_routes.route('/<id>')
def get_by_id(id):
    user = get_user_by_id(id)
    if not user:
        abort(404, 'User Not Found')
    user_dict = model_to_dict(user)
    user_dict.pop('password_hash')
    return jsonify(msg='User fetched successfully', user=user_dict), 200
