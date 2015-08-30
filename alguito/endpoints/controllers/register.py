# Functions defined here implement controller endpoints related to registration.
# For endpoints (URLs) see app.add_url_rule calls in in /alguito/app.py
from flask import render_template, request, session


# GET handler for registration page
# app.add_url_rule('/register/register', '/register/register/GET', register.register, methods=['GET'])
def register():
    session['test'] = 'Passed!'
    return render_template('login/register.html', active_tab="register")

def login():
    return render_template('login/login.html')

# POST handler for registration page
# app.add_url_rule('/register/register', '/register/register/POST', register.handle_register, methods=['POST'])
def handle_register():
    session['test'] = 'Passed!'
    return render_template('login/register.html', active_tab="register")