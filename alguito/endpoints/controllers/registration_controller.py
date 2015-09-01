# Functions defined here implement controller endpoints related to registration.
# For endpoints (URLs) see app.add_url_rule calls in in /alguito/app.py
from flask import render_template, request, session
from alguito.model.registration_model import RegistrationModel

# GET handler for registration page
# app.add_url_rule('/register/register', '/register/register/GET', register.register, methods=['GET'])
def register():
    return render_template('login/register.html', active_tab="register")

def login():
    return render_template('login/login.html')

# POST handler for registration page
# app.add_url_rule('/register/register', '/register/register/POST', register.handle_register, methods=['POST'])
def handle_register():
    model = RegistrationModel(None)
    email, password, password2, teamName = \
        request.form["inputEmail"], request.form["inputPassword"], request.form["inputPassword2"], request.form["inputTeamName"]
    error = model.register_new_account(email, password, password2, teamName)
    if not error:
        heading="Registered"
        message="Registration succeeded.  Now go have coffee!"
    else:
        heading, message = get_error_message(error)

    return render_template('login/register_result.html', active_tab="register", heading=heading, message=message)

def get_error_message(error):
    general_error_heading = "Registration Error"
    errors = dict({ \
        RegistrationModel.ERROR_DUPLICATE_TEAM: (general_error_heading, "The account name you have chosen is already in use."), \
        RegistrationModel.ERROR_PASSWORD_MISMATCH: (general_error_heading, "The passwords you entered do not match."), \
        # Note this one needs instructions for retrieving password...
        RegistrationModel.ERROR_DUPLICATE_EMAIL: (general_error_heading, "The email address you entered is already in use in our system.  Please enter a different email.") \
        })
    return errors.get(error) or  ('General Registration Error', 'Sorry, but we were unable to complete your registration.  We are working to resolve the issue. Please try again later.')