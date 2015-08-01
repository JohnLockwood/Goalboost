from eve import Eve
from flask import render_template

app = Eve(__name__, settings="alguito/endpoints/eve/settings.py")

@app.route('/')
def index():
    # return app.send_static_file('index.html') -- use this if in static dir
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
