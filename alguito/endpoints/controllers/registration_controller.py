# import flask
# from alguito.endpoints.forms.login_form import LoginForm
# import alguito.auth
# import flask.ext.login
#
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         user = alguito.auth.User(form.email.data, form.password.data)
#         flask.ext.login.login_user(user)
#         flask.flash('Logged in successfully.')
#         next = flask.request.args.get('next')
#             # next_is_valid should check if the user has valid
#         # permission to access the `next` url
#         #if not next_is_valid(next):
#         #    return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#
#     return flask.render_template('login/login.html',
#                            title='Sign In',
#                            form=form)
