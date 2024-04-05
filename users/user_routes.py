from flask import Blueprint, request, jsonify
from utils import model_to_dict
from .user_service import *
from app.middlewares.authentication import authenticate_user


user_routes = Blueprint('user_routes', __name__)


@user_routes.before_request
def authenticate_before_request():
    authenticate_user()


@user_routes.route('me')
def get_me():
    user_dict = model_to_dict(request.user)
    user_dict.pop('password_hash')
    return jsonify(msg='User fetched successfully', user=user_dict), 200


@user_routes.route('<id>')
def get_by_id(id):
    user = get_user_by_id(id)
    user_dict = model_to_dict(user)
    user_dict.pop('password_hash')
    return jsonify(msg='User fetched successfully', user=user_dict), 200


@user_routes.route('', methods=['GET'])
def get_all():
    # get query parameters
    query_params = request.args.to_dict()
    users = get_all_users(query_params)
    users_list = [model_to_dict(user) for user in users]
    for user in users_list:
        user.pop('password_hash')
    return jsonify(msg='Users fetched successfully', users=users_list), 200
