# Functions defined here implement controller endpoints related to registration.
# For endpoints (URLs) see app.add_url_rule calls in in /alguito/app.py
from flask import render_template, request, session



def register():
    session['test'] = 'Passed!'
    return render_template('login/register.html', active_tab="Tabzilla The Fun!")

def login():
    return render_template('login/login.html')