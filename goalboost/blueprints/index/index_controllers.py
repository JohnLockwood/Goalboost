# Import flask dependencies
from flask import Blueprint, redirect, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
from flask.ext.login import current_user

bp_index = Blueprint('index', __name__, url_prefix='/')

# Set the route and accepted methods
@bp_index.route('', methods=['GET'])
def index():
    return render_template("index/index.html", userId="")

@bp_index.route('development', methods=['GET'])
def development():
    u = current_user
    return render_template("index/development.html")

@bp_index.route('test', methods=['GET'])
def test():
    u = current_user
    return render_template("index/test.html")

