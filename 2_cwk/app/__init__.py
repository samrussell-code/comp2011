from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

migrate = Migrate(app, db)

from app import views, models
# >>> with app.app_context(): models.Property.query.filter_by(duration=5).all()