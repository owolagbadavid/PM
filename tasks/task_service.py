from app import db
from db.models import Task, Project, User, Status
from utils.validate_json import validate_json
from .task_schemas import task_schema, task_query_schema
from projects.project_service import get_project_by_id
from users.user_service import get_user_by_id
from werkzeug.exceptions import UnprocessableEntity, HTTPException, NotFound
from db import session
from datetime import datetime


def get_task_by_id(project_id, id: int) -> Task:
    task: Task = Task.query.get_or_404(id, 'Task Not Found')
    if task.project_id != project_id:
        raise NotFound('Task Not Found')
    return task


def get_all_tasks(project_id, query_params=None) -> Task:
    if query_params:
        try:
            validate_json(query_params, task_query_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    query = session.query(Task)

    page, count = 1, 10

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

    if 'page' in query_params:
        page = query_params['page']
    if 'count' in query_params:
        count = query_params['count']

    query = query.limit(count).offset((page - 1) * count)

    return query.all()


def create_task(task_dto, project_id, request_user: User):
    try:
        validate_json(task_dto, task_schema)
        project = get_project_by_id(project_id).is_manager_or_403(request_user)
        task = Task(name=task_dto['name'], description=task_dto['description'], start_date=task_dto['start_date'], end_date=task_dto['end_date'],
                    project_id=project_id)
        users = []
        for user_id in task_dto['user_ids']:
            user = get_user_by_id(user_id)
            if user not in project.contributors:
                raise UnprocessableEntity(
                    f'User {user.first_name} {user.last_name} is not a contributor to this project! Add as a contibutor first')
            users.append(user)
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
    print(task.owned_project)
    return task


def update_task_by_id(project_id, id, task_dto, request_user: User):
    try:
        validate_json(task_dto, task_schema)

        project = get_project_by_id(project_id).is_manager_or_403(request_user)

        task: Task | None = next(
            (task for task in project.tasks if task.id == id), None)
        if not task:
            raise NotFound('Task Not Found')

        task.name = task_dto['name']
        task.description = task_dto['description']
        task.start_date = task_dto['start_date']
        task.end_date = task_dto['end_date']
        task.assigned_to = []
        users = []
        for user_id in task_dto['user_ids']:
            user = get_user_by_id(user_id)
            if user not in project.contributors:
                raise UnprocessableEntity(
                    f'User {user.first_name} {user.last_name} is not a contributor to this project! Add as a contibutor first')
            users.append(user)
        for user in users:
            task.assigned_to.append(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Task could not be updated')

    return task


def update_task_status_by_id(project_id, id, status, request_user: User):
    try:
        task = get_task_by_id(project_id, id).is_assigned_or_403(request_user)
        if status == 'completed' and task.status != Status.COMPLETED.value:
            task.status = Status.COMPLETED.value
            task.completed_date = datetime.now()
        elif status == 'pending':
            task.status = Status.PENDING.value
            task.completed_date = None
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Task status could not be updated')
    return task


def delete_task_by_id(project_id, id, request_user: User):
    try:
        project = get_project_by_id(project_id).is_manager_or_403(request_user)

        task = next((task for task in project.tasks if task.id == id), None)
        if not task:
            raise NotFound('Task Not Found')
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Task could not be deleted')
    return task
