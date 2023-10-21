from flask_wtf import FlaskForm
from wtforms import IntegerField,FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CalculatorForm(FlaskForm):
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])

class MoneyForm(FlaskForm):
    type = SelectField('Transaction Type',choices=["Income","Expenditure"])
    name = TextAreaField('Name',validators=[DataRequired()])
    amount = FloatField('Amount',validators=[DataRequired(),NumberRange(min=0.01, max=9.0e12)])

class GoalForm(FlaskForm):
    name = TextAreaField('Name')
    amount = FloatField('Amount',validators=[DataRequired(),NumberRange(min=0.01, max=9.0e12)]) 

class SubmitForm(FlaskForm):
    submit = SubmitField('submit')