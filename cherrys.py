"""
Cherrys is a Redis backend for CherryPy sessions.

The redis server must support SETEX http://redis.io/commands/setex.

Relies on redis-py https://github.com/andymccurdy/redis-py.
"""

import threading

try:
  import cPickle as pickle
except ImportError:
  import pickle

from cherrypy.lib.sessions import Session
import redis

class RedisSession(Session):

    # the default settings
    host = '127.0.0.1'
    port = 6379
    db = 0
    password = None

    @classmethod
    def setup(cls, **kwargs):
        """Set up the storage system for redis-based sessions.

        Called once when the built-in tool calls sessions.init.
        """
        # overwritting default settings with the config dictionary values
        for k, v in kwargs.items():
            setattr(cls, k, v)

        cls.cache = redis.Redis(
            host=cls.host,
            port=cls.port, # cherrys in charge of converting str to int
            db=cls.db,
            password=cls.password)

    def _exists(self):
        return bool(self.cache.exists(self.id))

    def _load(self):
        try:
          return pickle.loads(self.cache.get(self.id))
        except TypeError:
          # if id not defined pickle can't load None and raise TypeError
          return None

    def _save(self, expiration_time):

        pickled_data = pickle.dumps(
            (self._data, expiration_time),
            pickle.HIGHEST_PROTOCOL)

        result = self.cache.setex(self.id, pickled_data, self.timeout * 60)

        if not result:
            raise AssertionError("Session data for id %r not set." % self.id)

    def _delete(self):
        self.cache.delete(self.id)

    # http://docs.cherrypy.org/dev/refman/lib/sessions.html?highlight=session#locking-sessions
    # session id locks as done in RamSession

    locks = {}

    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        self.locked = True
        self.locks.setdefault(self.id, threading.RLock()).acquire()

    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        self.locks[self.id].release()
        self.locked = False

