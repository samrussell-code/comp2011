from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)
from app import views, models

#when running from terminal use
#from app import app
#with app.app_context():

#to modify data entries, modify the variable entered into the table
#or db.session.query().filter().update()