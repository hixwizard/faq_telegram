from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
)
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import func


class Base(DeclarativeBase):

    """Базовый класс для моделей."""

    pass


class User(Base):

    """Модель пользователя."""

    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)  # ID из Telegram
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(
        Enum('user', 'admin', 'operator', name='role_enum'),
        default='user'
    )  # Роль: user, admin, operator
    is_blocked = Column(Boolean, default=False)
    applications = relationship("Application", back_populates="user")


class Application(Base):

    """Модель заявок клиента."""

    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    status_id = Column(
        Integer, ForeignKey('questions_status.id'), nullable=False
    )
    questions = Column(String, nullable=False)  # Ответы клиента на вопросы
    user = relationship("User", back_populates="applications")
    status = relationship("QuestionsStatus", back_populates="applications")


class QuestionsStatus(Base):

    """Модель статусов заявки."""

    __tablename__ = 'questions_status'
    id = Column(Integer, primary_key=True)
    status = Column(
        Enum('открыта', 'в работе', 'закрыта', name='status_enum'),
        nullable=False
    )
    applications = relationship("Application", back_populates="status")


class QuestionsCheckStatus(Base):

    """Модель логов изменений статусов заявок."""

    __tablename__ = 'questions_check_status'
    id = Column(Integer, primary_key=True)
    application_id = Column(
        Integer, ForeignKey('applications.id'), nullable=False
    )
    modified_by = Column(String, ForeignKey('user.id'))  # Кто изменил
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())


class Question(Base):

    """Модель вопросов."""

    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)  # Порядок вопросов
    question = Column(String, nullable=False)
