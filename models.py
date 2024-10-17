from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()


class ApplicationStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    is_blocked = Column(Integer, default=False)
    applications = relationship("ApplicationModel", back_populates="user")


class ApplicationModel(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="applications")
    business_type = Column(String, nullable=False)
    current_restrictions = Column(String, nullable=False)
    goals = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class ApplicationLog(Base):
    __tablename__ = 'application_logs'

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.id'))
    old_status = Column(Enum(ApplicationStatus))
    new_status = Column(Enum(ApplicationStatus))
    changed_by = Column(Integer, ForeignKey('users.id'))
    changed_at = Column(DateTime, default=datetime.utcnow)
