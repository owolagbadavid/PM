from app import db, bcrypt
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey, Column, DateTime, Enum
import enum
from werkzeug.exceptions import Forbidden


workspace_admin_association_table = db.Table('workspace_admin',
                                             Column('adminstrator_id', Integer, ForeignKey(
                                                 'users.id'), primary_key=True),
                                             Column('workspace_id', Integer, ForeignKey(
                                                 'workspaces.id'), primary_key=True)
                                             )

project_manager_association_table = db.Table('project_manager',
                                             Column('manager_id', Integer, ForeignKey(
                                                 'users.id'), primary_key=True),
                                             Column('project_id', Integer, ForeignKey(
                                                 'projects.id'), primary_key=True)
                                             )

project_contributor_association_table = db.Table('project_contributor',
                                                 Column('contibutor_id', Integer, ForeignKey(
                                                     'users.id'), primary_key=True),
                                                 Column('project_id', Integer, ForeignKey(
                                                     'projects.id'), primary_key=True)
                                                 )

task_assignment_association_table = db.Table('task_assignment',
                                             Column('assigned_to_id', Integer, ForeignKey(
                                                 'users.id'), primary_key=True),
                                             Column('task_id', Integer, ForeignKey(
                                                 'tasks.id'), primary_key=True)
                                             )


class Status(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class User(db.Model):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name = mapped_column(type_=String(length=30), nullable=False)

    last_name = mapped_column(type_=String(length=30), nullable=False)

    email = mapped_column(type_=String(
        length=50), nullable=False, unique=True
    )
    password_hash = mapped_column(type_=String(length=60), nullable=False)

    @property
    def password(self):
        self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class WorkSpace(db.Model):

    __tablename__ = 'workspaces'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(type_=String(length=30), nullable=False)
    description = mapped_column(type_=String(length=100))

    administrators = relationship(
        'User', secondary=workspace_admin_association_table, backref='workspaces')

    projects = relationship('Project', backref='owned_workspace', lazy=True)

    def is_admin_or_403(self, user: User):
        if user not in self.administrators:
            raise Forbidden('You are not an admin of this workspace')
        return self


class Project(db.Model):

    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(type_=String(length=30), nullable=False)
    description = mapped_column(type_=String(length=100))
    start_date = mapped_column(type_=DateTime)
    end_date = mapped_column(type_=DateTime)

    managers = relationship(
        'User', secondary=project_manager_association_table, backref='managed_projects')

    contributors = relationship(
        'User', secondary=project_contributor_association_table, backref='projects')

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey('workspaces.id'), nullable=True)

    tasks = relationship('Task', backref='owned_project', lazy=True)

    def is_manager_or_403(self, user: User):
        if user not in self.managers:
            raise Forbidden('You are not a manager of this project')
        return self

    def is_contributor_or_403(self, user: User):
        if user not in self.contributors:
            raise Forbidden('You are not a contributor of this project')
        return self


class Task(db.Model):

    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(type_=String(length=30), nullable=False)
    description = mapped_column(type_=String(length=100))
    start_date = mapped_column(type_=DateTime)
    end_date = mapped_column(type_=DateTime)

    status: Mapped[Status] = mapped_column(
        Enum('pending', 'completed', name='status'), default=Status.PENDING.value, )

    completed_date = mapped_column(type_=DateTime)

    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id'), nullable=True)

    assigned_to = relationship(
        'User', secondary=task_assignment_association_table, backref='tasks')

    def is_assigned_or_403(self, user: User):
        if user not in self.assigned_to:
            raise Forbidden('You are not assigned to this task')
        return self
