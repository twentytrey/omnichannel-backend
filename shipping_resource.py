from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever
from ops.calculations.calculations import (Calcode,Calcodedesc,Stencalusg,Calrule,Calscale,Calscaleds,Crulescale,
        Calrange,Calrlookup)
from ops.shipping.shipping import (Shpjcrule,EntryException,ShpCalrule,MethodsFromCalcode,Shipmode,Shipmodclcd,
        Shipmodedsc,Shparrange,Shparjurgp,ShippingPolicy,ReadCharge)
from ops.trading.trading import Policy,Policydesc
from ops.payment.payment import ReadPolicyTc

class create_shipcharge(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_calmethod_id",help="required field",required=True)
        self.parser.add_argument("calcode_calmethod_id_app",help="required field",required=True)
        self.parser.add_argument("calcode_calmethod_id_qfy",help="required field",required=True)
        self.parser.add_argument("calcode_code",help="required field",required=True)
        self.parser.add_argument("calcode_description",help="required field",required=True)
        self.parser.add_argument("calrange_calmethod_id",help="required field",required=True)
        self.parser.add_argument("calrange_rangestart",help="required field",required=True)
        self.parser.add_argument("calrange_value",help="required field",required=True)
        self.parser.add_argument("calrule_calcode_id",help="required field",required=True)
        self.parser.add_argument("calrule_calmethod_id",help="required field",required=True)
        self.parser.add_argument("calrule_calmethod_id_qfy",help="required field",required=True)
        self.parser.add_argument("calrule_ffmcenter_id",help="required field",required=True)
        self.parser.add_argument("calrule_jurstgroup_id",help="required field",required=True)
        self.parser.add_argument("calscale_calmethod_id",help="required field",required=True)
        self.parser.add_argument("calscale_calrule_id",help="required field",required=True)
        self.parser.add_argument("calscale_calusage_id",help="required field",required=True)
        self.parser.add_argument("calscale_code",help="required field",required=True)
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(create_shipcharge,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calcode_calmethod_id=data["calcode_calmethod_id"]
        calcode_calmethod_id_app=data["calcode_calmethod_id_app"]
        calcode_calmethod_id_qfy=data["calcode_calmethod_id_qfy"]
        calcode_code=data["calcode_code"]
        calcode_description=data["calcode_description"]
        calrange_calmethod_id=data["calrange_calmethod_id"]
        calrange_rangestart=data["calrange_rangestart"]
        calrange_value=data["calrange_value"]
        calrule_calcode_id=data["calrule_calcode_id"]
        calrule_calmethod_id=data["calrule_calmethod_id"]
        calrule_calmethod_id_qfy=data["calrule_calmethod_id_qfy"]
        calrule_ffmcenter_id=data["calrule_ffmcenter_id"]
        calrule_jurstgroup_id=data["calrule_jurstgroup_id"]
        calscale_calmethod_id=data["calscale_calmethod_id"]
        calscale_calrule_id=data["calscale_calrule_id"]
        calscale_calusage_id=data["calscale_calusage_id"]
        calscale_code=data["calscale_code"]
        storeent_id=data["storeent_id"]
        language_id=data["language_id"]
        try:
            calcode_id=Calcode(calcode_code,calscale_calusage_id,storeent_id,calcode_calmethod_id,calcode_calmethod_id_app,calcode_calmethod_id_qfy,lastupdate=datetimestamp_now(),description=calcode_description).save()
            Calcodedesc(calcode_id,language_id,calcode_description).save()
            calrule_id=Calrule(calcode_id,calrule_calmethod_id,calrule_calmethod_id_qfy,field2=calcode_description,).save()
            Shpjcrule(calrule_id,ffmcenter_id=calrule_ffmcenter_id,jurstgroup_id=calrule_jurstgroup_id,).save()
            calscale_id=Calscale(storeent_id,calscale_calusage_id,calscale_calmethod_id,code="{}/{}".format(calscale_code,calrule_id),description=calcode_description,field1=calcode_description).save()
            Crulescale(calscale_id,calrule_id).save()
            calrange_id=Calrange(calrange_calmethod_id,calscale_id=calscale_id,rangestart=calrange_rangestart).save()
            Calrlookup(calrange_id,value=calrange_value).save()
            return {"status":"OK","msg":"Successfully saved shipping charge",
            "charges":ReadCharge(storeent_id,calscale_calusage_id).read()},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

class read_charges(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("calusage_id",help="required field",required=True)
        super(read_charges,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        calusage_id=data["calusage_id"]
        return ReadCharge(storeent_id,calusage_id).read(),200

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

class ship_charges(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("jurstgroup_id",help="required field",required=True)
        self.parser.add_argument("storeent_id",help="required field",required=True)
        super(ship_charges,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        jurstgroup_id=data["jurstgroup_id"]
        storeent_id=data["storeent_id"]
        return ReadCharge.readcode(storeent_id,jurstgroup_id),200

class create_shipmode_policy(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_id",help="required field",required=True)
        self.parser.add_argument("carrier",help="required field",required=True)
        self.parser.add_argument("code",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("policytype_id",help="required field",required=True)
        self.parser.add_argument("enddate")
        self.parser.add_argument("ffmcenter_id",help="required field",required=True)
        self.parser.add_argument("jurstgroup_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("startdate")
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("timelimited",help="required field",required=True)
        super(create_shipmode_policy,self).__init__()
    
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
        policytype_id=data["policytype_id"]
        storeent_id=data["storeent_id"]
        timelimited=data["timelimited"]
        try:
            shipmode_id=Shipmode(storeent_id,code=code,carrier=carrier).save()
            Shipmodedsc(shipmode_id,language_id,description).save()
            shparrange_id=Shparrange(storeent_id,ffmcenter_id,shipmode_id,startdate,enddate).save()
            Shipmodclcd(storeent_id,calcode_id,shipmode_id).save()
            Shparjurgp(shparrange_id,jurstgroup_id).save()
            policy_id=Policy(description,policytype_id,storeent_id,None,startdate,enddate).save()
            Policydesc(policy_id,language_id,description,timecreated=datetimestamp_now(),timeupdated=datetimestamp_now()).save()
            shipmodes=ShippingPolicy(language_id,policytype_id).read()
            return {"msg":"Successfully saved shipping arrangement","shipmodes":shipmodes},200
        except EntryException as e:
            return {"msg":"Error: {}".format(e.message)}

class list_shipping_policies(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("policytype_id",required=True,help="required field")
        super(list_shipping_policies,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        policytype_id=data["policytype_id"]
        return ShippingPolicy(language_id,policytype_id).read(),200

class read_shipping_policy(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("tcsubtype_id",required=True,help="required field")
        self.parser.add_argument("trading_id",required=True,help="required field")
        super(read_shipping_policy,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        tcsubtype_id=data["tcsubtype_id"]
        trading_id=data["trading_id"]
        return ReadPolicyTc(trading_id,tcsubtype_id,language_id).get(),200
