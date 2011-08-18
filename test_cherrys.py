import unittest
import socket

import cherrypy
from cherrypy.test import webtest

# testing that redis-py is availbale and that we have a redis server running
try:
    import redis

    host, port = '127.0.0.1', 6379
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        s = None
        try:
            s = socket.socket(af, socktype, proto)
            s.settimeout(1.0)
            s.connect((host, port))
            s.close()
        except socket.error:
            if s:
                s.close()
            raise
        break

except ImportError:

  class RedisSessionTest(unittest.TestCase):
      def test_nothing(self):
          self.fail("redis-py not available")

except socket.error:

  class RedisSessionTest(unittest.TestCase):
      def test_nothing(self):
          self.fail("redis not reachable")

# all good to go we can test
else:

  import cherrys
  cherrypy.lib.sessions.RedisSession = cherrys.RedisSession

  class RedisSessionTest(webtest.WebCase):

      interactive = False

      def setUp(self):
          # configuring CP instead of webCase (getPage - openUrl on port 8000)
          cherrypy.config.update({
              'server.socket_port' : 8000,
              'log.screen' : False,
              'tools.sessions.on' : True,
              'tools.sessions.storage_type' : 'redis'
          })
          cherrypy.tree.mount(Root())
          cherrypy.engine.start()

      def test_server_working(self):
          self.getPage('/')
          self.assertStatus(200)

      def test_deleting_non_existing_key_fails(self):
          self.getPage('/delete')
          self.assertStatus(500)

      def test_storing_data(self):
          self.getPage('/store')
          self.assertStatus(200)
          self.assertBody('redis')

      def test_retrieving_stored_data(self):
          self.getPage('/retrieve')
          self.assertStatus(500)
          self.getPage('/store')
          self.assertStatus(200)
          self.assertBody('redis')
          self.getPage('/retrieve')
          self.assertStatus(200)

      def tearDown(self):
          cherrypy.engine.exit()

class Root(object):
    """ An basic application to test sessions """

    @cherrypy.expose
    def index(self):
        return 'index'

    @cherrypy.expose
    def store(self):
        cherrypy.session['data'] = 'redis'
        return cherrypy.session['data']

    @cherrypy.expose
    def delete(self):
        del cherrypy.session['data']

    @cherrypy.expose
    def retrieve(self):
        return cherrypy.session['data']

if __name__ == '__main__':
  unittest.main()
