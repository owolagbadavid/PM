from db.models import User
from app import db
from db import session
from utils.validate_json import validate_json
from .user_schemas import user_filter_schema
from werkzeug.exceptions import UnprocessableEntity


def create_user(user_dto):
    print('creating user', user_dto)
    try:
        user = User(**user_dto)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if 'unique constraint' in str(e):
            raise UnprocessableEntity(
                'User with that email already exists')
        raise e
    return user


def get_user_by_id(id: int) -> User:
    return User.query.get_or_404(id, 'User Not Found')


def get_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()


def get_all_users(query_params) -> User:
    if query_params:
        try:
            validate_json(query_params, user_filter_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    query = session.query(User)

    page, count = 1, 10

    if 'first_name' in query_params:
        query = query.filter(User.first_name.ilike(
            f"%{query_params['first_name']}%"))
    if 'last_name' in query_params:
        query = query.filter(User.last_name.ilike(
            f"%{query_params['last_name']}%"))
    if 'email' in query_params:
        query = query.filter(User.email.ilike(f"%{query_params['email']}%"))
    if 'page' in query_params:
        page = int(query_params['page'])
    if 'count' in query_params:
        count = int(query_params['count'])

    query = query.limit(count).offset((page - 1) * count)

    return query.all()
