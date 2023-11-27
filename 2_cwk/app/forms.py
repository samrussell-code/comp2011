from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo

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
    email = StringField('Email') # this field is never used because i didnt have time to implement it
    submit = SubmitField('Register')

class ReviewForm(FlaskForm):
    # rating is 0-100 intfield so i can constrain later to a 1dp float value between 0 and 10.0
    rating = IntegerField('Rating (1-100)', validators=[DataRequired(), NumberRange(1, 100)])
    title = StringField('Title')
    body = TextAreaField('Description')
    submit = SubmitField('Submit Review')
