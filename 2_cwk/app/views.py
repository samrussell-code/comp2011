from flask import render_template
from app import app

@app.route('/', methods=['GET', 'POST'])
def home():
    home = {'description': 'You can use this app to manage your money and set goals.',
            'optional_goal': 'You have no optional goal.',
            'null_money': 'You have no income or expenditure data.'}
    return render_template('home.html', title='Home', home=home)

