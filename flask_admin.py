from flask import Flask
from flask_admin import Admin
from database import engine
from models import Base

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
Base.metadata.create_all(bind=engine)

# Admin section
admin = Admin(app, name='Admin Zone', template_mode='bootstrap3')

if __name__ == '__main__':
    app.run(debug=True)
