# Import flask dependencies
from flask import Blueprint, redirect, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_index = Blueprint('index', __name__, url_prefix='/')

# Set the route and accepted methods
@mod_index.route('', methods=['GET'])
def index():
    return render_template("index.html")

@mod_index.route('foundation', methods=['GET'])
def fnd_eg():
    return render_template("home/foundation_example.html")

