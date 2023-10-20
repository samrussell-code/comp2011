from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])

class MoneyForm(FlaskForm):
    name = TextAreaField('Name',validators=[DataRequired()])
    amount = IntegerField('Amount',validators=[DataRequired()])