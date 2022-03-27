
from flask import request
from flask_restful import Resource
from bleach import clean

from .serializer import Ip, Globe

from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet as _DBSET


class IpRegistry(Resource):

    def __init__(self) -> None:
        self._db = _DBSET(sql_filename="geo.pgsql")

    @response
    def post(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        adr = Ip(ipaddr=request.form["remadr"])
        print(adr)

        with self._db.get_db(dict=True) as con:
            self._db._model.cr8_remotadr(con, remotaddr=adr.ipaddr)
            return 201
        
    @response
    def get(self):
        """reset password"""

        with self._db.get_db(dict=True) as con:
            self._db._model.remotadr(con, cr8_remotaddr=request.values)
            return 201


class Geodata(IpRegistry):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr):
        # get the post data
        prof_data = request.get_json() or request.form
        print(prof_data)
        if not (check:= Globe(
                    dspln=prof_data.get('dspln'), place=prof_data.get('plc'),
                    strtd=prof_data.get('strt'), endd=prof_data.get('end')
                )):
            return 401
        try:
            with self._db.get_db() as con:
                self._db._model.in_work(
                    con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),
                    strtd=check.strtd, endd=check.endd,
                )
            return 201
        except Exception:
            return 401

    @response
    @authenticate
    def get(self, usr):
        """reset password"""

        with self._db.get_db() as con:
            self._db._model.in_work(
                con, usr=usr
            )
            return 201
