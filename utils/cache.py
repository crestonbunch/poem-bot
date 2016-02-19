import sqlite3
import os.path

class Cache:

    def __init__(self, storage='sqlite', **kwargs):
        """Create a cache instance for storing and retrieving cached key,value
        pairs. Currently only supports an sqlite backend.

        Arguments:
            storage: The storage engine to use. Currently only supports sqlite,
                defaults to sqlite.
            path: Path to the cache file to use.
        """

        self.storage = storage
        if self.storage == 'sqlite' and 'path' not in kwargs:
            raise ValueError('SQLite cache needs a path argument.')
        elif self.storage == 'sqlite' and 'path' in kwargs:
            self.path = kwargs['path']
            # currently no database is set up, so let's make one
            if not os.path.isfile(self.path) or self.path == ':memory:':
                self.conn = sqlite3.connect(self.path)
                self._init_sqlite()
            else:
                # load sqlite connection at path
                self.conn = sqlite3.connect(self.path)

    def set(self, key, value):
        if self.storage == 'sqlite':
            c = self.conn.cursor()
            c.execute('''INSERT INTO cache SET key=?, value=?''', (key, value))
            self.conn.commit()

    def get(self, key):
        if self.storage == 'sqlite':
            c = self.conn.cursor()
            c.execute('''SELECT value FROM cache WHERE key = ?''', (key,))
            result = c.fetchone()
            if result is None: return result
            return result[0]

    def _init_sqlite(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT''')
        self.conn.commit()

