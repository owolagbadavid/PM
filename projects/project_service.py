from db.models import Project, User
from app import db
from werkzeug.exceptions import UnprocessableEntity, HTTPException
from utils.validate_json import validate_json
from .project_schemas import project_schema, project_filter_schema
from workspaces.workspace_service import get_workspace_by_id
from users.user_service import get_user_by_id
from db import session


def get_project_by_id(id: int) -> Project:
    return Project.query.get_or_404(id, 'Project Not Found')


def get_all_projects(query_params) -> Project:
    if query_params:
        try:
            validate_json(query_params, project_filter_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    query = session.query(Project)

    if 'name' in query_params:
        query = query.filter(Project.name.ilike(f"%{query_params['name']}%"))
    if 'description' in query_params:
        query = query.filter(Project.description.ilike(
            f"%{query_params['description']}%"))
    if 'start_date' in query_params:
        query = query.filter(Project.start_date >= query_params['start_date'])
    if 'end_date' in query_params:
        query = query.filter(Project.end_date <= query_params['end_date'])
    if 'workspace_id' in query_params:
        query = query.filter(Project.workspace_id ==
                             query_params['workspace_id'])

    return query.all()


def create_project(project_dto, user: User):
    try:
        validate_json(project_dto, project_schema)
        get_workspace_by_id(project_dto['workspace_id'])
        print(project_dto)
        project = Project(name=project_dto['name'], description=project_dto['description'],
                          start_date=project_dto['start_date'], end_date=project_dto['end_date'], workspace_id=project_dto['workspace_id'])
        project.managers.append(user)
        project.contributors.append(user)
        db.session.add(project)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Project could not be created')
    return project


def delete_project(id: int) -> Project:
    project = get_project_by_id(id)
    db.session.delete(project)
    db.session.commit()
    return project


def update_project(id: int, project_dto) -> Project:
    try:
        validate_json(project_dto, project_schema)
        project = get_project_by_id(id)
        project.name = project_dto['name']
        project.description = project_dto['description']
        project.start_date = project_dto['start_date']
        project.end_date = project_dto['end_date']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise UnprocessableEntity('Project could not be updated')
    return project


def add_manager_to_project(project_id: int, user_id: int):
    project = get_project_by_id(project_id)
    user = get_user_by_id(user_id)
    project.managers.append(user)
    db.session.commit()
    return project


def add_contributor_to_project(project_id: int, user_id: int):
    project = get_project_by_id(project_id)
    user = get_user_by_id(user_id)
    project.contributors.append(user)
    db.session.commit()
    return project
