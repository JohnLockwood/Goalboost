# Import flask dependencies
from flask import Blueprint, redirect, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_index = Blueprint('index', __name__, url_prefix='/')

# Set the route and accepted methods
@bp_index.route('', methods=['GET'])
def index():
    return render_template("index/index.html")

@bp_index.route('development', methods=['GET'])
def development():
    return render_template("index/development.html")

