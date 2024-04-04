from app import db
from db.models import Task, Project, User, Status
from utils.validate_json import validate_json
from .task_schemas import task_schema
from projects.project_service import get_project_by_id
from users.user_service import get_user_by_id
from werkzeug.exceptions import UnprocessableEntity, HTTPException


def get_task_by_id(id: int) -> Task:
    return Task.query.get_or_404(id, 'Task Not Found')


def get_all_tasks(filter) -> Task:
    return Task.query.filter_by(**filter).all()


def create_task(task_dto, project_id):
    try:
        validate_json(task_dto, task_schema)
        get_project_by_id(project_id)
        task = Task(name=task_dto['name'], description=task_dto['description'], start_date=task_dto['start_date'], end_date=task_dto['end_date'],
                    project_id=project_id, status=Status.PENDING.value)
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
