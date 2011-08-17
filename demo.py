import cherrypy
from cherrypy import _cperror

def handle_error():
    cherrypy.response.status = 500
    cherrypy.response.body = ["<html><body><pre>%s</pre></body></html>" % _cperror.format_exc()]

import cherrys
cherrypy.lib.sessions.RedisSession = cherrys.RedisSession

cherrypy.config.update({
                        #'server.socket_host': '0.0.0.0', #if you are running this on ec2, uncomment
                        #'server.socket_port': 8080,      #so you can access by host address
                        'request.error_response': handle_error,
                        'tools.sessions.on': True,
                        'tools.sessions.storage_type': "redis",
                        'tools.sessions.timeout': 60,
                        })

class RedisExample(object):
    def __init__(self):
        pass

    def index(self):
        return "index"
    index.exposed = True

    def report(self):
        counter = cherrypy.session['counter']
        return "count: %d" % counter
    report.exposed = True

    def add(self):
        counter = cherrypy.session.get('counter', 0) + 1
        cherrypy.session['counter'] = counter
        return "added count: %d" % counter
    add.exposed = True

cherrypy.quickstart(RedisExample())
