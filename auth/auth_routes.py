from flask import Blueprint, request, jsonify
from .auth_service import login_service, register_service
from werkzeug.exceptions import HTTPException

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/login', methods=['POST'])
def login():
    # Authentication logic
    try:
        data = request.json
        token = login_service(data)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify(msg="Login Successful", token=token), 200


@auth_routes.route('/register', methods=['POST'])
def register():
    # REGISTER logic
    try:
        data = request.json
        token = register_service(data)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify(msg="Registration Successful", token=token), 201
