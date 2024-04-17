from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest
from app.middlewares.authentication import authenticate_user
from .project_service import *
from tasks.task_service import *
from utils import model_to_dict

project_routes = Blueprint('project_routes', __name__)


@project_routes.before_request
def authenticate_before_request():
    authenticate_user()


@project_routes.route('<int:id>', methods=['GET'])
def get_by_id(id: int):
    project = get_project_by_id(id)
    project_dict = model_to_dict(project)
    if project.tasks:
        tasks = [model_to_dict(task) for task in project.tasks]
        project_dict['tasks'] = tasks

    return jsonify({'msg': 'Project Found Successfully', 'project': project_dict}), 200


@project_routes.route('', methods=['GET'])
def get_all():
    query_params = request.args.to_dict()
    projects = get_all_projects(query_params)
    return jsonify({'msg': 'Projects Found Successfully', 'projects': [model_to_dict(project) for project in projects]}), 200


@ project_routes.route('', methods=['POST'])
def create():
    try:
        data = request.json
        project = create_project(data, request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Project Created Successfully', 'project': model_to_dict(project)}), 201


@project_routes.route('<int:id>', methods=['DELETE'])
def delete(id: int):
    project = delete_project(id, request.user)
    return jsonify({'msg': 'Project Deleted Successfully', 'project': model_to_dict(project)}), 200


@project_routes.route('<int:id>', methods=['PUT'])
def update(id: int):
    try:
        data = request.json
        project = update_project(id, data, request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Project Updated Successfully', 'project': model_to_dict(project)}), 200


@project_routes.route('<int:project_id>/add_manager/<int:user_id>', methods=['PATCH'])
def add_manager(project_id: int, user_id: int):
    project = add_manager_to_project(project_id, user_id, request.user)
    return jsonify({'msg': 'Manager Added Successfully', 'project': model_to_dict(project)}), 200


@project_routes.route('<int:project_id>/add_contributor/<int:user_id>', methods=['PATCH'])
def add_contributor(project_id: int, user_id: int):
    project = add_contributor_to_project(
        project_id, user_id, request_user=request.user)
    return jsonify({'msg': 'Contributor Added Successfully', 'project': model_to_dict(project)}), 200

# remove manager from project


@project_routes.route('<int:project_id>/remove_manager/<int:user_id>', methods=['PATCH'])
def remove_manager(project_id: int, user_id: int):
    project = remove_manager_from_project(
        project_id, user_id, request_user=request.user)
    return jsonify({'msg': 'Manager Removed Successfully', 'project': model_to_dict(project)}), 200

# remove contributor from project


@project_routes.route('<int:project_id>/remove_contributor/<int:user_id>', methods=['PATCH'])
def remove_contributor(project_id: int, user_id: int):
    project = remove_contributor_from_project(
        project_id, user_id, request_user=request.user)
    return jsonify({'msg': 'Contributor Removed Successfully', 'project': model_to_dict(project)}), 200


@project_routes.route('<int:project_id>/add_task', methods=['PATCH'])
def add_task(project_id: int):
    try:
        data = request.json
        task = create_task(data, project_id, request_user=request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Task Created Successfully', 'task': model_to_dict(task)}), 201


@project_routes.route('<int:project_id>/tasks/<int:task_id>', methods=['GET'])
def task_by_id(project_id, task_id):
    task = get_task_by_id(project_id, task_id)
    task_dict = model_to_dict(task)

    task_dict['assigned_to'] = [model_to_dict(
        user) for user in task.assigned_to]
    # delete user.password_hash
    for user in task_dict['assigned_to']:
        del user['password_hash']
    return jsonify({'msg': 'Task fetched Successfully', 'task': task_dict})


@project_routes.route('<int:project_id>/tasks', methods=['GET'])
def all_tasks(project_id):
    query_params = request.args.to_dict()
    tasks = get_all_tasks(project_id, query_params)
    return jsonify({'msg': 'Tasks fetched Successfully', 'tasks': [model_to_dict(task) for task in tasks]})


@project_routes.route('<int:project_id>/tasks/<int:task_id>', methods=['PUT'])
def update_task(project_id, task_id):
    try:
        data = request.json
        task = update_task_by_id(
            project_id, task_id, data, request_user=request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Task Updated Successfully', 'task': model_to_dict(task)}), 200


@project_routes.route('<int:project_id>/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(project_id, task_id):
    task = delete_task_by_id(project_id, task_id, request_user=request.user)
    return jsonify({'msg': 'Task Deleted Successfully', 'task': model_to_dict(task)}), 200


@project_routes.route('<int:project_id>/tasks/<int:task_id>/update_status', methods=['PATCH'])
def update_task_status(project_id, task_id):
    try:
        data = request.json
        if 'status' not in data:
            raise BadRequest('Status is required')
        if data['status'] not in ['pending', 'completed']:
            raise BadRequest('Invalid Status')
        status = data['status']
        task = update_task_status_by_id(
            project_id, task_id, status, request_user=request.user)
    except HTTPException as e:
        return jsonify(error=e.description), e.code
    return jsonify({'msg': 'Task Status Updated Successfully', 'task': model_to_dict(task)}), 200
