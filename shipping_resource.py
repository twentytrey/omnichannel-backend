from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.calculations.calculations import Calcode,Calcodedesc,Stencalusg,Calrule,Calscale,Calscaleds,Crulescale,Calrange,Calrlookup
from ops.shipping.shipping import (Shpjcrule,EntryException,ShpCalrule,MethodsFromCalcode,Shipmode,Shipmodclcd,Shipmodedsc,Shparrange,
Shparjurgp)

class create_shpcalrule(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_id",help="required",required=True)
        self.parser.add_argument("calmethod_id",help="required",required=True)
        self.parser.add_argument("calmethod_id_qfy",help="required",required=True)
        self.parser.add_argument("ffmcenter_id",help="required",required=True)
        self.parser.add_argument("flags",help="required",required=True)
        self.parser.add_argument("jurstgroup_id",help="required",required=True)
        self.parser.add_argument("field2",help="required",required=True)
        super(create_shpcalrule,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calcode_id=data["calcode_id"]
        calmethod_id=data["calmethod_id"]
        calmethod_id_qfy=data["calmethod_id_qfy"]
        ffmcenter_id=data["ffmcenter_id"]
        flags=data["flags"]
        jurstgroup_id=data["jurstgroup_id"]
        field2=data["field2"]
        try:
            calrule_id=Calrule(calcode_id,calmethod_id,calmethod_id_qfy,flags=flags,field2=field2).save()
            Shpjcrule(calrule_id,ffmcenter_id,jurstgroup_id).save()
            return {"msg":"Successfully saved calculation rule","calruledata":ShpCalrule.read()},200
        except EntryException as e:
            return {"msg":"Error saving tax calculation rule. Error {0}".format(e.message)},422

class read_shpcalrule(Resource):
    @jwt_required
    def get(self):return ShpCalrule.read(),200

class methods_from_calcode(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_id",help="required field",required=True)
        super(methods_from_calcode,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calcode_id=data["calcode_id"]
        return MethodsFromCalcode(calcode_id).getmethods(),200

class create_shipmode(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_id",help="required field",required=True)
        self.parser.add_argument("carrier",help="required field",required=True)
        self.parser.add_argument("code",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("enddate")
        self.parser.add_argument("ffmcenter_id",help="required field",required=True)
        self.parser.add_argument("jurstgroup_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("startdate")
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("timelimited",help="required field",required=True)
        super(create_shipmode,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calcode_id=data["calcode_id"]
        carrier=data["carrier"]
        code=data["code"]
        description=data["description"]
        enddate=data["enddate"]
        ffmcenter_id=data["ffmcenter_id"]
        jurstgroup_id=data["jurstgroup_id"]
        language_id=data["language_id"]
        startdate=data["startdate"]
        storeent_id=data["storeent_id"]
        timelimited=data["timelimited"]
        if timelimited=="No":
            startdate=timestamp_now()
            enddate=timestamp_forever()
        try:
            shipmode_id=Shipmode(storeent_id,code=code,carrier=carrier).save()
            Shipmodedsc(shipmode_id,language_id,description).save()
            shparrange_id=Shparrange(storeent_id,ffmcenter_id,shipmode_id,startdate,enddate).save()
            Shipmodclcd(storeent_id,calcode_id,shipmode_id).save()
            Shparjurgp(shparrange_id,jurstgroup_id).save()
            return {"msg":"Successfully saved shipping arrangement"},200
        except EntryException as e:
            return {"msg":"Error: {}".format(e.message)}
