from flask_wtf import FlaskForm
from wtforms import FloatField, RadioField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

# form for adding an income or expenditure entry


class MoneyForm(FlaskForm):
    type = RadioField('Transaction Type', choices=[
                      "Income", "Expenditure"], default="Income", validators=[DataRequired()])
    name = TextAreaField('Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[
                        DataRequired(), NumberRange(min=0.01, max=9.0e12)])

# form for setting a goal


class GoalForm(FlaskForm):
    name = TextAreaField('Name')
    amount = FloatField('Amount', validators=[
                        DataRequired(), NumberRange(min=0.01, max=9.0e12)])

# form for deleting a goal


class DeleteForm(FlaskForm):
    submit = SubmitField('submit')

# form for changing an entry in the income table


class ModifyIncomeForm(FlaskForm):
    id = SelectField('Income ID', validators=[DataRequired()], choices=[])
    name = StringField('Name', validators=[Optional()])
    amount = FloatField('Amount', validators=[
                        Optional(), NumberRange(min=0.01, max=9.0e12)])
    submit = SubmitField('Save Changes')

# form for changing an entry in the expenditure table


class ModifyExpenditureForm(FlaskForm):
    id = SelectField('Income ID', validators=[DataRequired()], choices=[])
    name = StringField('Name', validators=[Optional()])
    amount = FloatField('Amount', validators=[
                        Optional(), NumberRange(min=0.01, max=9.0e12)])
    submit = SubmitField('Save Changes')
