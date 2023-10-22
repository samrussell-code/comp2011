from flask import redirect, render_template, flash, request, url_for
from app import app, db, models
from .forms import ModifyIncomeForm, MoneyForm, GoalForm, SubmitForm

@app.route('/home', methods =['GET','POST'])
def home():

    goal_set=False
    goal_name=""
    goal_amount=-1.0
    goal_progress=-1.0

    with app.app_context():
        expenditure_query=db.session.query(models.Expenditure.amount).all()
        income_query=db.session.query(models.Income.amount).all()
        if db.session.query(models.Goal).count()!=0:
            goal_set=True
            goal = db.session.query(models.Goal).first()
            goal_name, goal_amount = goal.name, goal.amount
    expenditure_total=0
    income_total=0
    for x in expenditure_query:
       expenditure_total+=float(x[0])
    for x in income_query:
        income_total+=float(x[0])
    exp_inc_dif = income_total-expenditure_total
    if goal_amount != -1.0:
        #goal exists
        goal_progress=max(round(100*(exp_inc_dif/goal_amount),2),0)
        #can go over 100 but the jinja if handles it
    home={'description':'Welcome to this application. We are here to set your goals!',
          'income_total':'This is your income total.',
          'optional_goal':'You have no optional goal.',
          'null_money':'This is to be shown if there is nothing to report.'}
    return render_template('home.html', title='Home', home=home, expenditure_total=expenditure_total, income_total=income_total, exp_inc_dif=exp_inc_dif, goal_name=goal_name, goal_amount=goal_amount, goal_set=goal_set, goal_progress=goal_progress) #this is the base location

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
    modify_form=ModifyIncomeForm()
    with app.app_context():
        incomes_list=db.session.query(models.Income).all()
    for x in incomes_list:
        modify_form.id.choices.append(x.id)
    incomes_count = len(incomes_list)
    incomes={'description':'This is incomes!'}
    if (modify_form.name.data or modify_form.amount.data) and modify_form.validate_on_submit():
        with app.app_context():
            income_entry=db.session.query(models.Income).filter_by(id=modify_form.id.data).first()
            income_entry.name=income_entry.name if not modify_form.name.data else modify_form.name.data
            income_entry.amount=income_entry.amount if not modify_form.amount.data else modify_form.amount.data
            try:
                db.session.commit()
            except:
                flash("Name is not unique!")
    return render_template('incomes.html', title='Incomes',incomes_list = incomes_list, incomes_count=incomes_count ,incomes=incomes, modify_form=modify_form, id=modify_form.id.data) #this is the base location

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

@app.route('/goal', methods =['GET','POST'])
def goal():
    goalform = GoalForm()
    deletegoal = SubmitForm()
    goal = models.Goal()
    name =""
    amount=0.0

    with app.app_context():
        if db.session.query(models.Goal).count() == 0:
            goal_set=False 
        else:
            goal_set=True
            goal = db.session.query(models.Goal).first()
            name, amount = goal.name, goal.amount

    if goalform.name.data and goalform.validate_on_submit():
        entry = models.Goal(name=goalform.name.data, amount=goalform.amount.data)
        with app.app_context():
            if not goal_set:
                db.session.add(entry)
                db.session.commit()
                name, amount = goalform.name.data, goalform.amount.data
            else:
                flash("You already have a goal set!")
        goal_set=True
        

    # 2 forms means extra validation is required to differentiate
    # which one was submitted
    elif not goalform.amount.data and deletegoal.validate_on_submit():
        with app.app_context():
            db.session.delete(goal)
            db.session.commit()
        goal_set=False
    
    return render_template('goal.html', title='Goal', name=name, amount=amount, goalform=goalform,goal_set=goal_set,deletegoal=deletegoal) #this is the base location

@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    with app.app_context():
        income_to_delete = models.Income.query.get(id)
        if income_to_delete:
            db.session.delete(income_to_delete)
            db.session.commit()
    return redirect(url_for('incomes'))

@app.route('/delete_expenditure/<int:id>', methods=['POST'])
def delete_expenditure(id):
    with app.app_context():
        expenditure_to_delete = models.Expenditure.query.get(id)
        if expenditure_to_delete:
            db.session.delete(expenditure_to_delete)
            db.session.commit()
    return redirect(url_for('expenditures'))

@app.route('/modify_income/<int:id>', methods=['POST'])
def modify_income(id):
    with app.app_context():
        income_to_delete = models.Expenditure.query.get(id)
        if income_to_delete:
            db.session.delete(income_to_delete)
            db.session.commit()
    return redirect(url_for('incomes'))