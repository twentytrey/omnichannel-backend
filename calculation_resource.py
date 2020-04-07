from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.calculations.calculations import Calcode,Calmethod,EntryException,Calcodedesc,Calscale,Calscaleds,Calrange,Calrlookup,Calusage
from ops.tax.tax import MethodsFromTaxcat,MethodFromCalscale

class read_calcodes(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("calusage_id",help="required",required=True)
        super(read_calcodes,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        calusage_id=data["calusage_id"]
        return Calmethod.read(storeent_id,calusage_id),200

class read_calmethods(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("calusage_id",help="required",required=True)
        super(read_calmethods,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        calusage_id=data["calusage_id"]
        return Calmethod.read(storeent_id,calusage_id),200

class methods_from_taxcat(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("taxcgry_id",help="required",required=True)
        super(methods_from_taxcat,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        taxcgry_id=data['taxcgry_id']
        return MethodsFromTaxcat(taxcgry_id).getmethods(),200

class read_calscale(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        super(read_calscale,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data['storeent_id']
        language_id=data['language_id']
        return Calscale.read(storeent_id,language_id),200

class read_calrange(Resource):
    @jwt_required
    def get(self):return Calrange.read(),200

class methods_from_calscale(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id")
        self.parser.add_argument("calscale_id")
        super(methods_from_calscale,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        calscale_id=data["calscale_id"]
        return MethodFromCalscale(calscale_id,storeent_id).getmethods(),200

class read_calusage(Resource):
    @jwt_required
    def get(self):
        return Calusage.read(),200

