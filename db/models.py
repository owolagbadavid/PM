from app import db, bcrypt
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey


class User(db.Model):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username = mapped_column(type_=String(length=30),
                             nullable=False, unique=True
                             )
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
