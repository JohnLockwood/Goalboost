# Functions defined here implement controller endpoints related to registration.
# For endpoints (URLs) see app.add_url_rule calls in in /alguito/app.py
from flask import render_template

def index():
    # return app.send_static_file('index.html') -- use this if in static dir
    # Or return "Hello world" for example to simply display a string
    return render_template('index.html')

# support Angular views with a route that resolves any given page in home directory
# So /home_index renders --> /home/index.html
def home(page):
    # For now
    return render_template('home/' + page + '.html')

