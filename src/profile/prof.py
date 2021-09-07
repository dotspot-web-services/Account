
from flask_restful import Resource
from flask import make_response, request
from bleach import clean

from profile.profSerializer import  (
    Basics, Acads,  Resrch,
    Workplace
)
from setting.decs import Auth as authenticate, Cors as corsify
from setting.dbcon import DbSet


class Basic(Resource):
    """
    basic education or acquired skill
    """

    def __init__(self):
        self._db = DbSet()

    @corsify
    @authenticate
    def post(self, usr):
        # get the post data
        bsic_data = request.get_json()
        
        check = Basics(
            dspln=bsic_data.get('displn'), place=bsic_data.get('plc'),
            strtd=bsic_data.get('strt'), endd=bsic_data.get('end'), acad=bsic_data.get('acad')
        )

        if isinstance(usr, tuple):
            return usr
        usr = usr[0].get('usr')
        with self._db.get_db() as con:
            data = self._db._model.in_basic(
                    con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place), 
                    strtd=check.strtd, endd=check.endd, acad=check.acad
                )
        #self._db.get_db().commit()

        try:
            #with self._db.get_db(dict=True) as con:
            
            #con.commit
            print(data)
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'failed', 'error': f'{data}'}, 401)
    
    @corsify
    def get(self):
        return make_response("this is a get request, it's reachable", 201)


class Accademics(Basic):
    """
    User Login Resource
    """

    @corsify
    @authenticate
    def post(self, usr):
        # get the post data
        acad_data = request.get_json()
        
        if self._db._model.acadqfn(self._db.get_db(), usr=usr):
            return make_response({'status': 'failed', 'message': 'not qualified for this profile'}, 401)

        check = Acads(
            arena=acad_data.get('base'), dspln=acad_data.get('displn'), place=acad_data.get('plc'),
            ttl=acad_data.get('ttl'), strtd=acad_data.get('strt'), endd=acad_data.get('end')
        )

        try:
            with self._db.get_db() as con:
                self._db._model.in_acad(
                    con, usr=usr, arena=check.arena, dspln=clean(check.dspln), plc=clean(check.place), 
                    ttl=clean(check.ttl), strt=check.strtd, endd=check.endd
                )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

    def get():
        """reset password"""

class Resacher(Accademics):
    """
    Logout Resource
    """
    
    @corsify
    @authenticate
    def post(self, usr):
        # get the post data
        rsrch_data = request.get_json()
        
        if self._db._model.rsrchaqfn(self._db(dict=True), usr=usr):
            return make_response({'status': 'failed', 'message': 'not qualified for this profile'}, 401)

        check = Resrch(
            acad=rsrch_data.get('acadlevl'), org=rsrch_data.get('institn'), dspln=rsrch_data.get('displn'), 
            eml=rsrch_data.get('emal'), strtd=rsrch_data.get('strt'), endd=rsrch_data.get('end')
        )

        try:
            with self._db.get_db() as con:
                self._db._model.in_rsrcha(
                    con, usr=usr, acad=check.acad, org=clean(check.org), dspln=clean(check.displn), 
                    strtd=check.strtd, endd=check.endd, typ=check.typ
                )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

class Works(Resacher):
    """
    basic education or acquired skill
    """

    @corsify
    @authenticate
    def post(self, usr):
        # get the post data
        prof_data = request.get_json()
        
        check = Workplace(
            arena=prof_data.get('arn'), plc=prof_data.get('plc'), rol=prof_data.get('rol'), 
            strtd=prof_data.get('strt'), endd=prof_data.get('end')
        )

        try:
            with self._db.get_db() as con:
                self._db._model.in_work(
                    con, usr=usr, arena=check.arena, plc=clean(check.plc), rol=clean(check.rol), 
                    strt=check.strtd, endd=check.endd
                )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)