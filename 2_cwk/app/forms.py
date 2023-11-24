from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, RadioField, StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional, EqualTo

# form for adding an income or expenditure entry

class AddMovieForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class SearchMovieForm(FlaskForm):
    movie_name = StringField('search', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    submit = SubmitField('submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    email = StringField('Email')
    submit = SubmitField('Register')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (0-100)', validators=[DataRequired(), NumberRange(0, 100)])
    title = StringField('Title')
    body = TextAreaField('Description')
    submit = SubmitField('Submit Review')
