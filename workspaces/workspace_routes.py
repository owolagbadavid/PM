from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from app.middlewares.authentication import authenticate_user
from workspaces.workspace_service import *
from utils import model_to_dict

workspace_routes = Blueprint('workspace_routes', __name__)


@workspace_routes.before_request
def authenticate_before_request():
    authenticate_user()


@workspace_routes.route('<int:id>', methods=['GET'])
def get_by_id(id: int):
    workspace = get_workspace_by_id(id)
    workspace_dict = model_to_dict(workspace)
    if workspace.administrators:
        administrators = [model_to_dict(project)
                          for project in workspace.administrators]
        # del password from user dict
        for admin in administrators:
            del admin['password_hash']
        workspace_dict['adminstrators'] = administrators
    return jsonify({'msg': 'Workspace Found Successfully', 'workspace': workspace_dict}), 200


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
    workspace = delete_workspace(id, request_user=request.user)
    return jsonify({'msg': 'Workspace Deleted Successfully', 'workspace': model_to_dict(workspace)}), 200


@workspace_routes.route('<int:id>', methods=['PUT'])
def update(id: int):
    try:
        data = request.json
        workspace = update_workspace(id, data, request_user=request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Workspace Updated Successfully', 'workspace': model_to_dict(workspace)}), 200


@workspace_routes.route('<int:workspace_id>/add_administrator/<int:user_id>', methods=['PATCH'])
def add_administrator(workspace_id: int, user_id: int):
    workspace = add_administrator_to_workspace(
        workspace_id, user_id, request_user=request.user)
    return jsonify({'msg': 'Administrator Added Successfully', 'workspace': model_to_dict(workspace)}), 200
