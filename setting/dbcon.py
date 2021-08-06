
import datetime
from functools import wraps

import jwt
from psycopg2 import connect
from anosql import from_path
from pydantic.types import FilePath
from flask import g, jsonify
from werkzeug.wrappers import request

from .base.setting import SpotSettings, CheckSet


#PGDB_URI = "postgres://QuestMasterDb:tFAtf6hCXdRhfWZ@questdb.cugmxolkmuvk.us-east-2.rds.amazonaws.com:5432/quest"

class DbSet:
    """"""
    def __init__(self, sql_file_path=None) -> None:
        self.sql: FilePath = sql_file_path
    _model = ""
    oda = CheckSet()

    @property
    def sql(self):
        return self.sql

    @sql.setter
    def sql(self, sq):
        if sq is None:
            sq = 'setting/sql/acct.sql'
        self._model = from_path(sql_path=sq, driver_name='psycopg2')

    @staticmethod
    def __conxn():
        try:
            return connect(SpotSettings().dict().get('pg_dsn'))
        except Exception as err:
            print(err)        

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.__conxn()
        return db

    #@app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

class Auth(DbSet):
    """decode auth and check validity"""

    def encode_auth(self, usr):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': usr
            }
            return jwt.encode(payload, self.oda.secret, algorithm='HS256')
        except Exception as e:
            return e

    
    def authenticate(self, func, *args, **kwargs):
        @wraps(func)
        def decode_auth():
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing'})
            try:
               data = jwt.decode(token, self.oda.secret)
               usr = self._model.get_usr(self.get_db(), usr=data['public_id'])
            except:
                return jsonify({'message': 'Token is invalid'}), 401
            return func(usr, args, kwargs)
        return decode_auth

if __name__ == "__main__":
    pg = DbSet()
    print(pg.__conxn())
