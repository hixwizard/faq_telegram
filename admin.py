from sqlalchemy.future import select
from models import (
    User, Application, Question, QuestionsStatus, QuestionsCheckStatus
)
from database import get_db_session  # Синхронная сессия для админки
from flask import Blueprint, render_template, redirect, url_for, request

admin = Blueprint('admin', __name__)


@admin.route('/admin/block_user/<user_id>', methods=['POST'])
def block_user(user_id):
    with get_db_session() as session:  # Синхронная работа с базой
        user = session.get(User, user_id)
        if user:
            user.is_blocked = True
            session.commit()
    return redirect(url_for('admin.user_list'))


@admin.route('/admin/unblock_user/<user_id>', methods=['POST'])
def unblock_user(user_id):
    with get_db_session() as session:
        user = session.get(User, user_id)
        if user:
            user.is_blocked = False
            session.commit()
    return redirect(url_for('admin.user_list'))


@admin.route('/admin/questions', methods=['GET', 'POST'])
def manage_questions():
    with get_db_session() as session:
        if request.method == 'POST':
            question_text = request.form['question']
            number = request.form['number']
            question = Question(number=number, question=question_text)
            session.add(question)
            session.commit()
        result = session.execute(
            select(Question).order_by(Question.number)
        )
        questions = result.scalars().all()
        return render_template('admin_questions.html', questions=questions)


@admin.route('/admin/application_status/<app_id>', methods=['POST'])
def update_application_status(app_id):
    with get_db_session() as session:
        application = session.get(Application, app_id)
        old_status = application.status.name
        new_status = request.form['status']
        application.status = QuestionsStatus[new_status]
        log = QuestionsCheckStatus(
            application_id=app_id, modified_by='admin',
            old_status=old_status, new_status=new_status
        )
        session.add(log)
        session.commit()
    return redirect(url_for('admin.application_list'))
