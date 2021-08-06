
#from typing import List
from flask_restful import Resource
from flask import make_response, request
#from pydantic import ValidationError, parse_obj_as
import bleach

from user.grocerySerializer import  (
    CreateAward, CreateStoryvasn, Createpub, CreateQuote, CreateStory,
)
from setting.dbcon import DbSet as db, Auth

authenticate = Auth.authenticate

class Awards(Resource):
    """
    User Resource
    """

    @authenticate
    def post(self, usr):
        # get the post data
        awd_data = request.get_json()
        
        check = CreateAward(
            typ=awd_data.get('typ'), arena=awd_data.get('arn'), org=awd_data.get('orgsatn'),
            pix=awd_data.get('med'), awdt=awd_data.get('dt'), 
        )

        try:
            db._model.in_awd(
                db, usr=usr, typ=check.typ, arena=check.arena, org=bleach(check.org), 
                pix=check.med, awdt=check.awdt, dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)


class Pubs(Resource):
    """get all events with get request and insert event with post request"""

    @authenticate
    def post(self, usr):
        # get the post data
        pub_data = request.get_json()
        
        check = Createpub(
            rsrch=pub_data.get('srch'), dfld=pub_data.get('fld'), dttl=pub_data.get('titl'),
            fyl=pub_data.get('fyl'), pdt=pub_data.get('pdt')
        )

        try:
            db._model.in_pub(
                db, usr=usr, srch=check.rsrch, fld=bleach(check.dfld), ttl=bleach(check.dttl), 
                fyl=check.med, pdt=check.pdt, dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)


class Story(Resource):
    """get all events with get request and insert event with post request"""

    @authenticate
    def post(self, usr):
        # get the post data
        stry_data = request.get_json()
        
        check = CreateStory(
            titl=stry_data.get('ttl'), sumry=stry_data.get('brifn')
        )

        try:
            db._model.in_stry(
                db, usr=usr, ttl=bleach(check.title), sumry=bleach(check.sumry), dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

class versn(Resource):
    """get all events with get request and insert event with post request"""

    @authenticate
    def post(self, usr):
        # get the post data
        vason_data = request.get_json()
        
        check = CreateStoryvasn(
            stry=vason_data.get('stry'), addin=vason_data.get('addin'), title=vason_data.get('ttl'),
            vason=vason_data.get('vsn'), refdt=vason_data.get('dt')
        )

        try:
            db._model.in_vasn(
                db, usr=usr, stry=check.stry, trib=check.adding, ttl=bleach(check.title),
                vasn=bleach(check.vason), vasndt=check.refdt, dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)   
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)

class Quote(Resource):
    """get all events with get request and insert event with post request"""

    @authenticate
    def post(self, usr):
        # get the post data
        qot_data = request.get_json()
        
        check = CreateQuote(
            vasn=qot_data.get('vasn'), qot=qot_data.get('qt')
        )

        try:
            db._model.in_qot(
                db, usr=usr, vason=check.vasn, qot=bleach(check.qot), dt=check.dt
            )
            return make_response({'status': 'successful'}, 201)
            
        except Exception as e:
            return make_response({'status': 'successful', 'error': f'{e}'}, 201)
