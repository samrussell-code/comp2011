from flask import render_template, flash
from app import app, db, models
from .forms import CalculatorForm, MoneyForm

@app.route('/home', methods =['GET','POST'])
def home():
    home={'description':'Welcome to this application. We are here to set your goals!',
          'expenditure_total':'This is your total expenditures.',
          'income_total':'This is your income total.',
          'exp_inc_dif':'This is the difference between your income and your expenditures.',
          'optional_goal':'This is your optional goal.',
          'null_money':'This is to be shown if there is nothing to report.'}
    return render_template('home.html', title='Home', home=home) #this is the base location

# @app.route('/calculator', methods=['GET', 'POST'])
# def calculator():
#     form = CalculatorForm()
#     if form.validate_on_submit():
#         flash('Succesfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
#     return render_template('calculator.html',
#                            title='Calculator',
#                            form=form)

@app.route('/expenditures', methods =['GET','POST'])
def expenditures():
    #grab the number of entries in db
    with app.app_context():
        expenditures_list=db.session.query(models.Expenditure).all()
    expenditures_count = len(expenditures_list)
    expenditures={'description':'This is expenditures!',
          'expenditure_table':"This should be a table of expenditures"}
    return render_template('expenditures.html', title='Expenditures', expenditures_list = expenditures_list,expenditures=expenditures, expenditures_count=expenditures_count) #this is the base location

@app.route('/incomes', methods =['GET','POST'])
def incomes():
    with app.app_context():
        incomes_list=db.session.query(models.Income).all()
    incomes_count = len(incomes_list)
    incomes={'description':'This is incomes!'}
    return render_template('incomes.html', title='Incomes',incomes_list = incomes_list, incomes_count=incomes_count ,incomes=incomes) #this is the base location

@app.route('/form', methods =['GET','POST'])
def form():
    databaseform = MoneyForm()
    if databaseform.validate_on_submit():
        flash('Received form data. %s'%(databaseform.type.data))
        if(databaseform.type.data=="Income"):
            entry = models.Income(name=databaseform.name.data, amount=databaseform.amount.data)
        else:
            entry = models.Expenditure(name=databaseform.name.data, amount=databaseform.amount.data)
        with app.app_context():
            try:
                db.session.add(entry)
                db.session.commit()
            except:
                flash("The name of this entry matches another entry in the table.")
        #now we add databaseform.name.data/amount to the correct table for type
    form={'description':'This is the expenditure income form!'}
    return render_template('form.html', title='Form', form=form, databaseform=databaseform) #this is the base location
