
#from functools import wraps
#from re import S

from psycopg2 import connect, extras
from aiosql import from_path
from pydantic.types import FilePath
from flask import g

from .base.setting import Settings, CheckSet


#PGDB_URI = "postgres://QuestMasterDb:tFAtf6hCXdRhfWZ@questdb.cugmxolkmuvk.us-east-2.rds.amazonaws.com:5432/quest"

class DbSet(object):
    """"""
    def __init__(self, sql_file_path=None):
        self.sql: FilePath = sql_file_path
        self._model = from_path(
            sql_path=self.sql, driver_adapter='psycopg2'
        )
    _oda = CheckSet()

    @property
    def sql(self):
        return self.__sql

    @sql.setter
    def sql(self, sq=None):
        if sq is None:
            self.__sql = 'src/setting/sql/acct.sql'

    # cursor_factory=extras.RealDictCursor        

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = connect(Settings().dict().get('pg_dsn'))
        db.cursor_factory = extras.NamedTupleCursor
        return db

    #@app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()


if __name__ == "__main__":
    pg = DbSet()
