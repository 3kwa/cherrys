import threading

try:
  import cPickle as pickle
except ImportError:
  import pickle

from cherrypy.lib.sessions import Session
import redis

class RedisSession(Session):

    locks = {}

    host = '127.0.0.1'
    port = 6379
    db = 0

    def setup(cls, **kwargs):
        """Set up the storage system for redis-based sessions.

        This should only be called once per process; this will be done
        automatically when using sessions.init (as the built-in Tool does).
        """
        for k, v in kwargs.items():
            setattr(cls, k, v)

        cls.cache = redis.Redis(host=cls.host, port=cls.port, db=cls.db)
    setup = classmethod(setup)

    def _exists(self):
        return bool(self.cache.get(self.id))

    def _load(self):
        return pickle.loads(self.cache.get(self.id))

    def _save(self, expiration_time):

        pickled_data = pickle.dumps(
            [self._data, expiration_time,
            pickle.HIGHEST_PROTOCOL])

        try:
          result = self.cache.setex(self.id, self.timeout * 60, pickled_data)
        except redis.ResponseError:
          result = self.cache.set(self.id, pickled_data)

        if not result:
            raise AssertionError("Session data for id %r not set." % self.id)

    def _delete(self):
        self.cache.delete(self.id)

    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        self.locked = True
        self.locks.setdefault(self.id, threading.RLock()).acquire()

    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        self.locks[self.id].release()
        self.locked = False

    def __len__(self):
        """Return the number of active sessions."""
        raise NotImplementedError


