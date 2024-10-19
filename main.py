from flask import Flask, request, jsonify
from models import User, Application, Question
from database import get_async_db_session
from sqlalchemy.future import select

app = Flask(__name__)


@app.route('/questions', methods=['GET'])
async def get_questions():

    """ json в качестве списка вопросов """

    async with get_async_db_session() as session:
        result = await session.execute(
            select(Question).order_by(Question.number)
        )
        questions = result.scalars().all()
        return jsonify(
            [{'number': q.number, 'question': q.question} for q in questions]
        )


@app.route('/submit_application', methods=['POST'])
async def submit_application():
    data = request.json
    async with get_async_db_session() as session:
        user = await session.get(User, data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        application = Application(
            user_id=user.id, status_id=1, questions=data['questions']
        )
        session.add(application)
        await session.commit()
        return jsonify({'message': 'Application submitted successfully'})


@app.route('/application_status/<int:app_id>', methods=['GET'])
async def get_application_status(app_id):
    async with get_async_db_session() as session:
        application = await session.get(Application, app_id)
        if application:
            return jsonify({'status': application.status.status})
        return jsonify({'error': 'Application not found'}), 404
