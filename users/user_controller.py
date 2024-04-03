from db.models import User
from app import db


def create_user(user_dto):
    print('creating user', user_dto)
    user = User(username=user_dto['username'],
                email=user_dto['email'], password=user_dto['password'])
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(id: int) -> User:
    return User.query.filter_by(id=id).first()


def get_user_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()
