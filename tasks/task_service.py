from app import db
from db.models import Task, Project, User, Status
from utils.validate_json import validate_json
from .task_schemas import task_schema, task_query_schema
from projects.project_service import get_project_by_id
from users.user_service import get_user_by_id
from werkzeug.exceptions import UnprocessableEntity, HTTPException
from db import session


def get_task_by_id(id: int) -> Task:
    return Task.query.get_or_404(id, 'Task Not Found')


def get_all_tasks(project_id, query_params=None) -> Task:
    if query_params:
        try:
            validate_json(query_params, task_query_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    query = session.query(Task)

    if 'name' in query_params:
        query = query.filter(Task.name.ilike(f"%{query_params['name']}%"))
    if 'description' in query_params:
        query = query.filter(Task.description.ilike(
            f"%{query_params['description']}%"))
    if 'start_date' in query_params:
        query = query.filter(Task.start_date >= query_params['start_date'])
    if 'end_date' in query_params:
        query = query.filter(Task.end_date <= query_params['end_date'])
    if 'status' in query_params:
        query = query.filter(
            Task.status == query_params['status'])
    query = query.filter(Task.project_id == project_id)
    return query.all()


def create_task(task_dto, project_id):
    try:
        validate_json(task_dto, task_schema)
        get_project_by_id(project_id)
        task = Task(name=task_dto['name'], description=task_dto['description'], start_date=task_dto['start_date'], end_date=task_dto['end_date'],
                    project_id=project_id)
        users = []
        for user_id in task_dto['user_ids']:
            users.append(get_user_by_id(user_id))
        print(users)
        for user in users:
            task.assigned_to.append(user)
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        print(f"{e}, error")
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Task could not be created')
    return task
