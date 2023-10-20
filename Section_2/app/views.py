from flask import render_template, flash
from app import app
from .forms import CalculatorForm #forms from cwd

@app.route('/')
def index():
    user = {'name': 'Sam Wilson'}
    return render_template('index.html',
                           title='Simple template example',
                           user=user)

@app.route('/fruit') # web path after the root
def displayFruit():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit.html",fruits=fruits)

@app.route('/calculator', methods=['GET','POST']) #more advanced path includes HTML methods
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        num1,num2=form.number1.data,form.number2.data
        flash('Successfully received form data. %s + %s = %s'%(num1,num2,num1+num2))
    return render_template('calculator.html', title='Calculator',form=form)
