from utils import verify_token
from flask import request, abort
from users.user_service import get_user_by_id
from workspaces.workspace_service import get_workspace_by_id
from projects.project_service import get_project_by_id
from tasks.task_service import get_task_by_id
from db.models import User


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


def authorize_user(resouce, resource_id, user: User):
    if resouce == 'workspace':
        workspace = get_workspace_by_id(resource_id)
        if user not in workspace.administrators:
            abort(403, 'Forbidden')
    elif resouce == 'project':
        project = get_project_by_id(resource_id)
        if user not in project.managers:
            abort(403, 'Forbidden')
    elif resouce == 'task':
        task = get_task_by_id(resource_id)
        if user not in task.assigned_to:
            abort(403, 'Forbidden')
