#!/usr/bin/env python3
from flask.ext.script import Manager, Shell

from goalboost.model import db
from goalboost import app
from goalboost.model.mongo_models import User, Timer

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def runserver_debug():
    app.run(debug=True)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Timer=Timer)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
