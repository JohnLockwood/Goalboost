#!/usr/bin/env python3
import os
from alguito import create_app
from alguito.datastore import db
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def runserver_debug():
    app.run(debug=True)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
