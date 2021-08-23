
from flask_restful import Resource
from flask import make_response, request
import bleach

from profile.profSerializer import  (
    Basic, Acads,  Resrch,
    Workplace
)
from setting.dbcon import DbSet as db, Auth

authenticate = Auth.authenticate

class Basic(Resource):
    """
    basic education or acquired skill
    """

    @authenticate
    def post(self, usr):
        # get the post data
        bsic_data = request.get_json()
        
        check = Basic(
            arena=bsic_data.get('arn'), dspln=bsic_data.get('displn'), place=bsic_data.get('plc'),
            strtd=bsic_data.get('strt'), endd=bsic_data.get('end')
        )

        try:
            db._model.in_basic(
                db, usr=usr, arena=check.arena, dspln=bleach(check.dspln), 
                plc=bleach(check.place), strt=check.strtd, endd=check.endd, dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

class Accademics(Resource):
    """
    User Login Resource
    """

    @authenticate
    def post(self, usr):
        # get the post data
        acad_data = request.get_json()
        
        if db._model.acadqfn(db, usr=usr):
            return make_response({'status': 'failed', 'message': 'not qualified for this profile'}, 401)

        check = Acads(
            arena=acad_data.get('arn'), dspln=acad_data.get('displn'), place=acad_data.get('plc'),
            strtd=acad_data.get('strt'), endd=acad_data.get('end'), ttl=acad_data.get('ttl')
        )

        try:
            db._model.in_acad(
                db, usr=usr, arena=check.arena, dspln=bleach(check.dspln), plc=bleach(check.plc), 
                strt=check.strtd, endd=check.endd, dt=check.dt, ttl=check.ttl
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

    def get():
        """reset password"""

class Resacher(Resource):
    """
    Logout Resource
    """
    
    @authenticate
    def post(self, usr):
        # get the post data
        rsrch_data = request.get_json()
        
        if db._model.rsrchaqfn(db, usr=usr):
            return make_response({'status': 'failed', 'message': 'not qualified for this profile'}, 401)

        check = Resrch(
            acad=rsrch_data.get('acadlevl'), org=rsrch_data.get('institn'), dspln=rsrch_data.get('displn'), 
            eml=rsrch_data.get('emal'), strtd=rsrch_data.get('strt'), endd=rsrch_data.get('end')
        )

        try:
            db._model.in_rsrcha(
                db, usr=usr, acad=check.acad, org=bleach(check.org), dspln=bleach(check.displn), 
                strtd=check.strtd, endd=check.endd, dt=check.dt, typ=check.typ
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

class Works(Resource):
    """
    basic education or acquired skill
    """

    @authenticate
    def post(self, usr):
        # get the post data
        prof_data = request.get_json()
        
        check = Workplace(
            arena=prof_data.get('arn'), plc=prof_data.get('plc'), rol=prof_data.get('rol'), 
            strtd=prof_data.get('strt'), endd=prof_data.get('end')
        )

        try:
            db._model.in_work(
                db, usr=usr, arena=check.arena, plc=bleach(check.plc), rol=bleach(check.rol), 
                strt=check.strtd, endd=check.endd, dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)