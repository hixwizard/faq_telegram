from flask_admin.contrib.sqla import ModelView
from models import User, Application, ApplicationLog
from .flask_admin import admin, session


def setup_admin(app):
    # Панель администратора для пользователей
    class UserAdminView(ModelView):
        column_list = ('id', 'name', 'email', 'phone', 'is_blocked')
        can_edit = True
        can_delete = True
        can_create = True

    # Панель администратора для заявок
    class ApplicationAdminView(ModelView):
        column_list = ('id', 'user', 'status', 'created_at', 'updated_at')
        can_edit = True
        can_delete = True
        can_create = True

    # Панель для логов заявок
    class ApplicationLogView(ModelView):
        column_list = (
            'application_id', 'old_status', 'new_status',
            'changed_by', 'changed_at'
        )
        can_create = False
        can_edit = False
        can_delete = False

    # Добавляем модели в админ-зону
    admin.add_view(UserAdminView(User, session))
    admin.add_view(ApplicationAdminView(Application, session))
    admin.add_view(ApplicationLogView(ApplicationLog, session))
