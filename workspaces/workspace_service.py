from db.models import WorkSpace
from app import db
from werkzeug.exceptions import UnprocessableEntity, HTTPException
from utils.validate_json import validate_json
from .workspace_schemas import *
from users.user_service import get_user_by_id
from db import session, subqueryload


def get_workspace_by_id(id: int) -> WorkSpace:
    return WorkSpace.query.get_or_404(id, 'Workspace Not Found')


def get_all_workspaces(query_params) -> WorkSpace:
    if query_params:
        try:
            validate_json(query_params, workspace_filter_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    page, count = 1, 10

    query = session.query(WorkSpace)

    if 'name' in query_params:
        query = query.filter(WorkSpace.name.ilike(f"%{query_params['name']}%"))
    if 'description' in query_params:
        query = query.filter(WorkSpace.description.ilike(
            f"%{query_params['description']}%"))
    if page in query_params:
        page = int(query_params['page'])
    if count in query_params:
        count = int(query_params['count'])

    query = query.limit(count).offset((page - 1) * count)

    return query.all()


def create_workspace(workspace_dto, user):
    try:
        validate_json(workspace_dto, workspace_schema)
        print(workspace_dto)
        workspace = WorkSpace(
            name=workspace_dto['name'], description=workspace_dto['description'])
        workspace.administrators.append(user)
        db.session.add(workspace)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Workspace could not be created')
    return workspace


def delete_workspace(id: int, request_user) -> WorkSpace:
    workspace = get_workspace_by_id(id).is_admin_or_403(request_user)
    db.session.delete(workspace)
    db.session.commit()
    return workspace


def update_workspace(id: int, workspace_dto, request_user) -> WorkSpace:
    try:
        validate_json(workspace_dto, workspace_schema)
        workspace = get_workspace_by_id(id).is_admin_or_403(request_user)
        workspace.name = workspace_dto['name']
        workspace.description = workspace_dto['description']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Workspace could not be updated')
    return workspace


def add_administrator_to_workspace(workspace_id: int, user_id: int, request_user):
    workspace = get_workspace_by_id(workspace_id).is_admin_or_403(request_user)
    user = get_user_by_id(user_id)
    workspace.administrators.append(user)
    db.session.commit()
    return workspace


def remove_administrator_from_workspace(workspace_id: int, user_id: int, request_user):
    workspace = get_workspace_by_id(workspace_id).is_admin_or_403(request_user)
    if user_id == request_user.id:
        raise UnprocessableEntity(
            'You cannot remove yourself as an administrator')
    user = get_user_by_id(user_id)
    workspace.administrators.remove(user)
    db.session.commit()
    return workspace
