import socket
import time
import threading

import cherrys
import cherrypy
import pytest
from cherrypy.test import helper


def setup_module():
    host, port = '127.0.0.1', cherrys.REDIS_PORT
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
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
            pytest.exit(f"Failed to connect to redis server", returncode=2)
        break


class RedisSessionTest(helper.CPWebCase):
    """RedisSession unittest class - connect to redis via hostname/port"""
    helper.CPWebCase.interactive = False

    @staticmethod
    def setup_server():
        cherrypy.config.update({
            'log.screen': False,  # set to True to see error stdout and errors from cp server
            'tools.sessions.on': True,
            'tools.session.host': "localhost",
            'tools.session.port': cherrys.REDIS_PORT,
            'tools.session.url': None,
            'tools.sessions.storage_class': cherrys.RedisSession
        })
        cherrypy.tree.mount(App())

    def test_server_working(self):
        self.getPage('/')
        self.assertStatus(200)

    def test_deleting_non_existing_key_fails(self):
        self.getPage('/delete')
        self.assertStatus(500)

    def test_deleting_stored_data(self):
        self.getPage('/store')
        self.assertStatus(200)
        # first getPage call sets a cookie
        # second getPage call needs to be aware of the cookie
        self.getPage('/delete', self.cookies)
        self.assertStatus(200)

    def test_storing_data(self):
        self.getPage('/store?sleep=5')
        self.assertStatus(200)
        self.assertBody('redis')

    def test_retrieving_stored_data(self):
        self.getPage('/retrieve')
        self.assertStatus(500)
        self.getPage('/store', self.cookies)
        self.assertStatus(200)
        self.assertBody('redis')
        self.getPage('/retrieve', self.cookies)
        self.assertStatus(200)

    def test_locked_session(self):
        """Check that redis really holds a lock on a session.

        This is achieved by sending two parallel requests with the same session id to
        the cherrypy server. The first request makes the session block for SLEEP_SECS.
        The second request should be forced to wait at least SLEEP_SECS before it
        can be accomplished.
        """
        SLEEP_SECS = 1.0
        self.getPage('/')
        # Cookies must be stored locally to be usable in background thread:
        cookies = self.cookies[:]
        thread = threading.Thread(
            target=self.getPage, args=[f'/store?sleep={SLEEP_SECS}', cookies]
        )
        thread.start()

        t0 = time.time()
        # Give background thread a chance to fire out the first request:
        time.sleep(SLEEP_SECS / 4)

        # Then launch the 2nd request with the same session id:
        self.getPage('/retrieve', cookies)
        # This check ensures that the 2nd request indeed had to wait until the first
        # request of the background thread (which blocked the session on the server
        # side) actually has finished:
        assert (time.time() - t0) >= SLEEP_SECS

        self.assertStatus(200)
        self.assertBody('redis')


class RedisSessionTestViaUrl(RedisSessionTest):
    """RedisSession unittest class - connect via redis-URL"""

    @staticmethod
    def setup_server():
        cherrypy.config.update({
            'log.screen': False,  # set to True to see error stdout and errors from cp server
            'tools.sessions.on': True,
            'tools.session.host': None,
            'tools.session.port': None,
            'tools.session.url': "redis://localhost:6379/0",
            'tools.sessions.storage_class': cherrys.RedisSession
        })
        cherrypy.tree.mount(App())


class App:
    """ A basic application to test sessions """
    app_data = None

    @cherrypy.expose
    def index(self):
        assert isinstance(cherrypy.serving.session, cherrys.RedisSession)
        cherrypy.session.load()
        return 'index'

    @cherrypy.expose
    def store(self, sleep=None):
        if sleep:
            time.sleep(float(sleep))
        cherrypy.session['data'] = 'redis'
        return cherrypy.session['data']

    @cherrypy.expose
    def delete(self):
        del cherrypy.session['data']
        return 'deleted'

    @cherrypy.expose
    def retrieve(self):
        return cherrypy.session['data']
