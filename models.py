import enum

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# --- Base for models ---
Base = declarative_base()


class User(Base):
    """
    Модель пользователя.
    """
    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # Telegram ID пользователя тип str
    name = Column(String, unique=True)
    phone = Column(String)
    email = Column(String)


class UserFormStatus(enum.Enum):
    """
    Модель статуса заявок.
    """
    open = 'Открыта'
    in_progress = 'В работе'
    closed = 'Закрыта'


class UserForm(Base):
    """
    Модель заявки.
    """
    __tablename__ = 'applications'

    id = Column(String, primary_key=True)
    status = Column(Enum(UserFormStatus), default=UserFormStatus.open)
    closed_by = Column(String, ForeignKey('users.name'))
    closed_by_user = relationship('User', backref='closed_applications')
