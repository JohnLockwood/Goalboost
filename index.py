import sys
sys.path.insert(0, "/home/johnlockwood/webapps/goalboost/htdocs")
from alguito import create_app
application = create_app('production')

'''
def application(environ, start_response):
    output = 'Welcome to your mod_wsgi website! It uses:\n\nPython %s' % sys.version
    output += '\nWSGI version: %s' % str(environ['mod_wsgi.version'])

    response_headers = [
        ('Content-Length', str(len(output))),
        ('Content-Type', 'text/plain'),
    ]

    start_response('200 OK', response_headers)

    return [bytes(output, 'utf-8')]
'''
