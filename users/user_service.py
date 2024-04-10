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
                'User with email or username already exists')
        raise e
    return user


def get_user_by_id(id: int) -> User:
    return User.query.get_or_404(id, 'User Not Found')


def get_user_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()


def get_all_users(query_params) -> User:
    if query_params:
        try:
            validate_json(query_params, user_filter_schema)
        except Exception as e:
            raise UnprocessableEntity('Invalid query parameters')

    query = session.query(User)

    if 'username' in query_params:
        query = query.filter(User.username.ilike(
            f"%{query_params['username']}%"))
    if 'email' in query_params:
        query = query.filter(User.email.ilike(f"%{query_params['email']}%"))

    return query.all()
