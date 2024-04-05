from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, NotFound, HTTPException
from app.middlewares.authentication import authenticate_user
from workspaces.workspace_service import *
from utils import model_to_dict

workspace_routes = Blueprint('workspace_routes', __name__)


@workspace_routes.before_request
def authenticate_before_request():
    authenticate_user()


@workspace_routes.errorhandler(Unauthorized)
def handle_unauthorized(error):
    response = jsonify(error=str(error))
    response.status_code = error.code
    return response


@workspace_routes.errorhandler(NotFound)
def handle_notfound(error):
    response = jsonify(error=str(error))
    response.status_code = error.code
    return response


@workspace_routes.route('<int:id>', methods=['GET'])
def get_by_id(id: int):
    workspace = get_workspace_by_id(id)
    return jsonify({'msg': 'Workspace Found Successfully', 'workspace': model_to_dict(workspace)}), 200


@workspace_routes.route('', methods=['GET'])
def get_all():
    query_params = request.args.to_dict()
    workspaces = get_all_workspaces(query_params)
    return jsonify({'msg': 'Workspaces Found Successfully', 'workspaces': [model_to_dict(workspace) for workspace in workspaces]}), 200


@workspace_routes.route('', methods=['POST'])
def create():
    try:
        data = request.json
        workspace = create_workspace(data, request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Workspace Created Successfully', 'workspace': model_to_dict(workspace)}), 201


@workspace_routes.route('<int:id>', methods=['DELETE'])
def delete(id: int):
    workspace = delete_workspace(id)
    return jsonify({'msg': 'Workspace Deleted Successfully', 'workspace': model_to_dict(workspace)}), 200


@workspace_routes.route('<int:id>', methods=['PUT'])
def update(id: int):
    try:
        data = request.json
        workspace = update_workspace(id, data)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Workspace Updated Successfully', 'workspace': model_to_dict(workspace)}), 200


@workspace_routes.route('<int:workspace_id>/add_administrator/<int:user_id>', methods=['PATCH'])
def add_administrator(workspace_id: int, user_id: int):
    workspace = add_administrator_to_workspace(workspace_id, user_id)
    return jsonify({'msg': 'Administrator Added Successfully', 'workspace': model_to_dict(workspace)}), 200
