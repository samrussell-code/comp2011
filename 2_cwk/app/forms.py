from flask_wtf import FlaskForm
from wtforms import FloatField, RadioField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

# form for adding an income or expenditure entry

class AddMovieForm(FlaskForm):
    name = TextAreaField('Name', validators=[DataRequired()])

class SearchMovieForm(FlaskForm):
    movie_name = StringField('search', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    submit = SubmitField('submit')