
#from functools import wraps
#from re import S

from psycopg2 import connect
from psycopg2.extras import RealDictCursor, NamedTupleCursor
from aiosql import from_path
from pydantic.types import FilePath
from flask import g
import redis

from .base.setting import Settings, CheckSet


#PGDB_URI = "postgres://QuestMasterDb:tFAtf6hCXdRhfWZ@questdb.cugmxolkmuvk.us-east-2.rds.amazonaws.com:5432/quest"

class DbSet(object):
    """"""
    def __init__(self, sql_filename:FilePath=None):
        """connect and load sql into aiosql for sql operations

        Args:
            sql_filename (string, optional): this must be the name of internal sql file. Defaults to None.
        """
        self.sql: FilePath = sql_filename
        if self.sql is None:
            self.__sql = '/home/johnmba/flaskproject/Account/src/setting/sql/acct.pgsql'
        else:
            self.__sql = f'/home/johnmba/flaskproject/Account/src/setting/sql/{self.sql}'
        self._model = from_path(
            sql_path=self.__sql, driver_adapter='psycopg2'
        )
    _oda = CheckSet()


    # cursor_factory=extras.RealDictCursor        

    def get_db(self, data_level:int=0):
        """the type of data to be loaded

        Args:
            data_level (int, optional): 1 for dict and 2 for namedtuple. Defaults to 0.

        Returns:
            [type]: [description]
        """

        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = connect(Settings().dict().get('pg_dsn'))
        if data_level == 1:
            db.cursor_factory = RealDictCursor
        if data_level == 2:
            db.cursor_factory = NamedTupleCursor
        return db
    
    def get_redis(self, db):
        """connect to redis database specifying the database number

        Args:
            db (int): the database to be connected with

        Returns:
           redis: connected redis database
        """
        
        redis_url = Settings().dict().get("redis_env_dsn")
        return redis.Redis(redis_url.format(db))

    async def access_cursor(self, query_obj):
        async with self.get_db() as conn:
            # append _cursor after query name
            async with query_obj(conn) as cur:
                print([col_info[0] for col_info in cur.description])
                first_row = await cur.fetchone()
                all_data = await cur.fetchall()
                print(f"ALL DATA: {all_data}") # list of tuples
                print(f"FIRST ROW: {first_row}") # tuple of first row d

    #@app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

def setdb():#
    #engine = create_engine('postgresql://accounts:napapaGod4me@localhost/accountsdb')
    pg_dns = {
        "host": "localhost",
        "port": 5432,
        "user": "accounts",
        "password": "napapaGod4me",
        "database": "accountsdb"
    }
    db = DbSet("table.pgsql")#database="test",
    with connect(**pg_dns) as con:
        db._model.cr8_schema(con)

if __name__ == "__main__":
    pg = DbSet()
