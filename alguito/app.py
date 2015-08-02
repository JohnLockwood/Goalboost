from eve import Eve
from flask import render_template
import os.path

here = os.path.dirname(os.path.realpath(__file__))

app = Eve(__name__, settings= here + "/endpoints/eve/settings.py")

@app.route('/')
def index():
    # return app.send_static_file('index.html') -- use this if in static dir
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "Hello, Alguito!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
