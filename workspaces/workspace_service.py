from db.models import WorkSpace
from app import db
from werkzeug.exceptions import UnprocessableEntity, HTTPException
from utils.validate_json import validate_json
from .workspace_schemas import workspace_schema
from users.user_service import get_user_by_id


def get_workspace_by_id(id: int) -> WorkSpace:
    return WorkSpace.query.get_or_404(id, 'Workspace Not Found')


def get_all_workspaces() -> WorkSpace:
    return WorkSpace.query.all()


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


def delete_workspace(id: int) -> WorkSpace:
    workspace = get_workspace_by_id(id)
    db.session.delete(workspace)
    db.session.commit()
    return workspace


def update_workspace(id: int, workspace_dto) -> WorkSpace:
    try:
        validate_json(workspace_dto, workspace_schema)
        workspace = get_workspace_by_id(id)
        workspace.name = workspace_dto['name']
        workspace.description = workspace_dto['description']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Workspace could not be updated')
    return workspace


def add_administrator_to_workspace(workspace_id: int, user_id: int):
    workspace = get_workspace_by_id(workspace_id)
    user = get_user_by_id(user_id)
    workspace.administrators.append(user)
    db.session.commit()
    return workspace
