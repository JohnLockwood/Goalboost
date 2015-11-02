import json
hours = """{"hours": [
{"contributor": "JohnLockwood", "date": "07/25/15", "hours": 3, "description": "Initial research and project creation"},
{"contributor": "JohnLockwood", "date": "07/26/15", "hours": 3, "description": "Continue preliminary work on Eve"},
{"contributor": "JohnLockwood", "date": "08/01/15", "hours": 3, "description": "Initial Bitbucket commit.  unit tests; work on idea project; test project generally"},
{"contributor": "JohnLockwood", "date": "08/02/15", "hours": 2, "description": "Create spec, Postman Testing"},
{"contributor": "JohnLockwood", "date": "08/03/15", "hours": 0.5, "description": "Add Team Entity and Test; create hours."},
{"contributor": "JohnLockwood", "date": "08/06/15", "hours": 0.5, "description": "Wrestle with an Eve configuration issue"},
{"contributor": "JohnLockwood", "date": "08/08/15", "hours": 3, "description": "Solve Eve configuration issue.  Preliminary bootstrap styling.  Fix paths to static and template files."},
{"contributor": "JohnLockwood", "date": "08/09/15", "hours": 1.75, "description": "Rework packages yet again.  Tests still hosed at this point.  Initial work on authentication, using alguitos as test endpoint."},
{"contributor": "JohnLockwood", "date": "08/14/15", "hours": 3, "description": "Begin writing auth tests.  Write function to encode basic auth headers.  Exercise Docstring mojo Remove settings.py in favor of inline settings in App. Preliminary Team+Password auth class."},
{"contributor": "JohnLockwood", "date": "08/15/15", "hours": 3, "description": "Demo Ipython notebooks for testing/documentation.  Rework people resource to begin using it as “User”."},
{"contributor": "JohnLockwood", "date": "08/16/15", "hours": 3, "description": "Create common unit test / integration test helper.  Begin work on integration test, SetupDemo.  Lot of good learning."},
{"contributor": "JohnLockwood", "date": "08/21/15", "hours": 0.5, "description": "Attempt to get authentication to work cleanly for superuser (site admin, god).  Moving in different direction."},
{"contributor": "JohnLockwood", "date": "08/22/15", "hours": 3, "description": "Set up Jinja templates including default layout, jquery version of active tab logic, and demo Flask session use, preliminary login and register pages.  Rework jquery version of active tab logic to Jinja to avoid flashing.  Create controllers package (really Jinja views); begin moving view code there."},
{"contributor": "JohnLockwood", "date": "08/23/15", "hours": 2.5, "description": "Incorporate Angular.js, with basic routing in place.  Still deciding on Angular Single Page App versus Jinja."},
{"contributor": "JohnLockwood", "date": "08/24/15", "hours": 1, "description": "Begin work on registration data model unit test and class."},
{"contributor": "JohnLockwood", "date": "08/29/15", "hours": 4, "description": "Work on registration page including Ajax call to verify team name; figure out how to get test request context (See TestHelper.test_request_context), and use this in new Auth test for now.  Additional methods on registration model."},
{"contributor": "JohnLockwood", "date": "08/30/15", "hours": 0.25, "description": "Work on wiring up registration view to model"},
{"contributor": "JohnLockwood", "date": "08/31/15", "hours": 0.75, "description": "Continue wiring up registration view to model"},
{"contributor": "JohnLockwood", "date": "09/01/15", "hours": 0.5, "description": "Registration view, registration model work."},
{"contributor": "JohnLockwood", "date": "09/20/15", "hours": 5, "description": "Better integration for SQLAlchemy, plus basic login working using flask-login + wtforms. Nice!"},
{"contributor": "JohnLockwood", "date": "09/21/15", "hours": 1.25, "description": "Work on fixing login bug; refactor auth into a Blueprint"},
{"contributor": "JohnLockwood", "date": "09/22/15", "hours": 0.25, "description": "Fix for login bug – working reasonably well now but need to get rid if blank password for logged in user."},
{"contributor": "JohnLockwood", "date": "09/26/15", "hours": 4, "description": "Refactoring, incorporate large app structure with config file, app factory, etc., and improve use of Blueprints."},
{"contributor": "JohnLockwood", "date": "09/27/15", "hours": 2, "description": "Re-incorporate Goalboost schema, rework unit tests."},
{"contributor": "JohnLockwood", "date": "09/27/15", "hours": 0.75, "description": "Use Flask-Security, replacing existing work on Flask-Login"},
{"contributor": "JohnLockwood", "date": "09/28/15", "hours": 0.5, "description": "Continue Flask-Security work"},
{"contributor": "JohnLockwood", "date": "09/28/15", "hours": 0.75, "description": "More flask-security work, now using Flask-Security, but more customization & cleanup to do!"},
{"contributor": "JohnLockwood", "date": "09/29/15", "hours": 0.5, "description": "Flask security customize login page somewhat."},
{"contributor": "JohnLockwood", "date": "09/30/15", "hours": 0.5, "description": "Redo schema Flask-Security + timer + task."},
{"contributor": "JohnLockwood", "date": "10/12/15", "hours": 2, "description": "Flask security / email configuration & testing.  Test basic signup (no confirmation yet)."},
{"contributor": "JohnLockwood", "date": "10/12/15", "hours": 1, "description": "Remove some sensitive information from repo."},
{"contributor": "JohnLockwood", "date": "10/13/15", "hours": 2, "description": "Continue removing sensitive stuff; rework for mongodb, replacing mysql in flask-security"},
{"contributor": "JohnLockwood", "date": "10/15/15", "hours": 1, "description": "Rework unit tests – passing under mongo.  Review flask-security datastore as basis for our models."},
{"contributor": "JohnLockwood", "date": "10/16/15", "hours": 1, "description": "Work on new mongo models, tests."},
{"contributor": "JohnLockwood", "date": "10/17/15", "hours": 1.5, "description": "Continue work on models and tests."}
]}
"""
obj = json.loads(hours)
print(obj)