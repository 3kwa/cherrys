import cherrypy
from cherrypy import _cperror

import cherrys

def handle_error():
    cherrypy.response.status = 500
    cherrypy.response.body = ["<html><body><pre>%s</pre></body></html>" % _cperror.format_exc()]

cherrypy.lib.sessions.RedisSession = cherrys.RedisSession

cherrypy.config.update({
                        'request.error_response': handle_error,
                        'tools.sessions.on': True,
                        'tools.sessions.storage_type': 'redis',
                        'tools.sessions.timeout': 60,
                        #'tools.sessions.host' : 'REDIS_HOST',
                        #'tools,sessions.port' : 'REDIS_PORT',
                        #'tools.sessions.db' : 'REDIS_DB',
                        #'tools.sessions.password' : 'REDIS_PASSWORD',
                        })

class RedisExample(object):
    def __init__(self):
        pass

    def index(self):
        return "index"
    index.exposed = True

    @cherrypy.expose
    def report(self):
        counter = cherrypy.session['counter']
        return "count: %d" % counter

    @cherrypy.expose
    def add(self):
        counter = cherrypy.session.get('counter', 0) + 1
        cherrypy.session['counter'] = counter
        return "added count: %d" % counter

    @cherrypy.expose
    def delete(self):
      del cherrypy.session['counter']
      return "counter deleted"


cherrypy.quickstart(RedisExample())
