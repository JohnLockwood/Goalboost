from flask_restful import Resource, Api
from flask import Flask, Response, redirect
import alguito.endpoints.controllers.registration_controller
from flask.ext.sqlalchemy import SQLAlchemy

from alguito.mod_auth.controllers import mod_auth as auth_module

# Flask-restful endpoints
#from alguito.endpoints.flask_restful.people import People, Person

# flask endpoints, i.e., web pages.
# For route information for these endpoints, see the app.add_url_rule calls further below
import alguito.endpoints.controllers.index as index
# import alguito.endpoints.controllers.registration_controller as register
app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Newacct1@localhost/alguito"
db = SQLAlchemy(app)

api = Api(app)





#login_manager = LoginManager()
#login_manager.init_app(app)



#@login_manager.user_loader
#def load_user_by_id(id):
#    return alguito.auth.load_user_by_id(id)


#app.add_url_rule('/login', '/login', alguito.endpoints.controllers.registration_controller.login, methods= ["GET", "POST"])

#login_manager.login_view = "/auth/login"

#@app.route("/logout")
#@login_required
#def logout():
#    logout_user()
#    return redirect("/")

# Register blueprint(s)
#app.register_blueprint(auth_module)


# But as long as you keep this in the root, everything works fine from a file, until it doesn't because
# of stupid import rules.
# app = Eve(__name__, settings='eve_')

# Define non-eve flask routes

# Non-eve flask routes are defined in functions in the package alguito.endpoints.controllers
# Routes are defined here.
app.add_url_rule('/', 'index', index.index)
app.add_url_rule('/home/<page>', '/home', index.home)


# Non-eve flask-restful resources

#class HelloWorldFlaskRestful(Resource):
#   def get(self):
#       return {'helloworld': 'HelloWorld from Flask Restful!'}

#api.add_resource(HelloWorldFlaskRestful, '/api/hello/')
#api.add_resource(People, '/api/people')
#api.add_resource(Person,  '/api/people/<string:id>')
#api.add_resource(People, '/api/people')


if __name__ == '__main__':
    app.run(debug=True, port=5001)



