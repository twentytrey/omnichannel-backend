from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.tax.tax import Jurstgprel,Jurst,Jurstgroup,Taxcgry,Taxcgryds,Taxjcrule,Taxtype,EntryException,TaxCalrule
from ops.calculations.calculations import Calcode,Calcodedesc,Stencalusg,Calrule,Calscale,Calscaleds,Crulescale,Calrange,Calrlookup

class read_jurst(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="compulsory field",required=True)
        self.parser.add_argument("subclass",help="compulsory field",required=True)
        super(read_jurst,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data['storeent_id']
        subclass=data['subclass']
        return Jurst.read(storeent_id,subclass)

class read_jurstgroup(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("subclass",help="required",required=True)
        super(read_jurstgroup,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        subclass=data["subclass"]
        return Jurstgroup.read(storeent_id,subclass)

class create_jurstgroup(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("description",help="required",required=True)
        self.parser.add_argument("subclass",help="required",required=True)
        self.parser.add_argument("code",help="required",required=True)
        self.parser.add_argument("storeent_id",help="required",required=True)
        super(create_jurstgroup,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        description=data['description']
        subclass=data['subclass']
        code=data['code']
        storeent_id=data['storeent_id']
        try:
            jurstgroup_id=Jurstgroup(subclass,storeent_id,code,description=description).save()
            return {"msg":"Successfully saved Jurisdiction Group","jgroups":Jurstgroup.read(storeent_id,subclass)},200
        except EntryException as e:
            return {"msg":"Error saving jurisdiction group. Error {0}".format(e.message)},422

class create_jurst(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("city")
        self.parser.add_argument("code",help="required",required=True)
        self.parser.add_argument("country",help="required",required=True)
        self.parser.add_argument("countryabbr",help="required",required=True)
        self.parser.add_argument("description",help="required",required=True)
        self.parser.add_argument("jurstgroup_id",help="required",required=True)
        self.parser.add_argument("state",help="required",required=True)
        self.parser.add_argument("stateabbr",help="required",required=True)
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("subclass",help="required",required=True)
        super(create_jurst,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        city=data['city']
        code=data['code']
        country=data['country']
        countryabbr=data['countryabbr']
        description=data['description']
        jurstgroup_id=data['jurstgroup_id']
        state=data['state']
        stateabbr=data['stateabbr']
        storeent_id=data['storeent_id']
        subclass=data['subclass']
        try:
            jurst_id=Jurst(storeent_id,code,subclass,country=country,description=description,
            city=city,state=state,stateabbr=stateabbr,countryabbr=countryabbr).save()
            Jurstgprel(jurst_id,jurstgroup_id,subclass).save()
            return {"msg":"Successfully saved jurisdiction","jurstdata":Jurst.read(storeent_id,subclass)},200
        except EntryException as e:
            return {"msg":"Error saving jurisdiction. Error {0}".format(e.message)},422

class read_taxtype(Resource):
    @jwt_required
    def get(self):return Taxtype.read(),200

class read_taxcgry(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        super(read_taxcgry,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        language_id=data["language_id"]
        return Taxcgry.read(storeent_id,language_id),200

class create_taxcgry(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("taxtype_id",help="required",required=True)
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("name",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        self.parser.add_argument("description",help="required",required=True)
        super(create_taxcgry,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        taxtype_id=data["taxtype_id"]
        storeent_id=data["storeent_id"]
        name=data["name"]
        language_id=data["language_id"]
        description=data["description"]
        try:
            taxcgry_id=Taxcgry(taxtype_id,storeent_id,name=name).save()
            Taxcgryds(language_id,taxcgry_id,description=description).save()
            return {"msg":"Successfully saved tax category","taxdata":Taxcgry.read(storeent_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error saving tax category. Error {0}".format(e.message)},422

class read_calcode(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        self.parser.add_argument("usages",action="append",help="required",required=True)
        super(read_calcode,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        storeent_id=data["storeent_id"]
        language_id=data["language_id"]
        usages=data["usages"]
        return Calcode.read(storeent_id,language_id,usages),200

class create_tax_calcode(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calmethod_id",help="required",required=True)
        self.parser.add_argument("calmethod_id_app",help="required",required=True)
        self.parser.add_argument("calmethod_id_qfy",help="required",required=True)
        self.parser.add_argument("calusage_id",help="required",required=True)
        self.parser.add_argument("code",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        self.parser.add_argument("description")
        self.parser.add_argument("storeent_id",help="required",required=True)
        super(create_tax_calcode,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calmethod_id=data["calmethod_id"]
        calmethod_id_app=data["calmethod_id_app"]
        calmethod_id_qfy=data["calmethod_id_qfy"]
        calusage_id=data["calusage_id"]
        code=data["code"]
        storeent_id=data["storeent_id"]
        description=data["description"]
        language_id=data["language_id"]
        try:
            calcode_id=Calcode(code,calusage_id,storeent_id,calmethod_id,calmethod_id_app,calmethod_id_qfy,
            lastupdate=timestamp_now()).save()
            Calcodedesc(calcode_id,language_id,description).save()
            Stencalusg.update_calcode(calcode_id,storeent_id,calusage_id)
            return {"msg":"Successfully saved {0}".format(description),"calcodedata":
            Calcode.read(storeent_id,language_id,[calusage_id])},200
        except EntryException as e:
            return {"msg":"Error saving {0}. Error {1}".format(description,e.message)},422

class read_taxcalrule(Resource):
    @jwt_required
    def get(self):return TaxCalrule.read(),200

class create_taxcalrule(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calcode_id",help="required",required=True)
        self.parser.add_argument("calmethod_id",help="required",required=True)
        self.parser.add_argument("calmethod_id_qfy",help="required",required=True)
        self.parser.add_argument("ffmcenter_id",help="required",required=True)
        self.parser.add_argument("flags",help="required",required=True)
        self.parser.add_argument("jurstgroup_id",help="required",required=True)
        self.parser.add_argument("taxcgry_id",help="required",required=True)
        super(create_taxcalrule,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calcode_id=data["calcode_id"]
        calmethod_id=data["calmethod_id"]
        calmethod_id_qfy=data["calmethod_id_qfy"]
        ffmcenter_id=data["ffmcenter_id"]
        flags=data["flags"]
        jurstgroup_id=data["jurstgroup_id"]
        taxcgry_id=data["taxcgry_id"]
        try:
            calrule_id=Calrule(calcode_id,calmethod_id,calmethod_id_qfy,taxcgry_id=taxcgry_id,flags=flags).save()
            Taxjcrule(calrule_id,ffmcenter_id,jurstgroup_id).save()
            return {"msg":"Successfully saved calculation rule","calruledata":TaxCalrule.read()},200
        except EntryException as e:
            return {"msg":"Error saving tax calculation rule. Error {0}".format(e.message)},422

class create_taxcalscale(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("code",help="required",required=True)
        self.parser.add_argument("calmethod_id",help="required",required=True)
        self.parser.add_argument("calusage_id",help="required",required=True)
        self.parser.add_argument("qtyunit_id",help="required",required=True)
        self.parser.add_argument("field1",help="required",required=True)
        self.parser.add_argument("setccurr",help="required",required=True)
        self.parser.add_argument("storeent_id",help="required",required=True)
        self.parser.add_argument("description",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        self.parser.add_argument("calrule_id",help="required",required=True)
        super(create_taxcalscale,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        code=data['code']
        calmethod_id=data['calmethod_id']
        calusage_id=data['calusage_id']
        qtyunit_id=data['qtyunit_id']
        field1=data['field1']
        setccurr=data['setccurr']
        storeent_id=data['storeent_id']
        description=data['description']
        language_id=data['language_id']
        calrule_id=data['calrule_id']
        try:
            calscale_id=Calscale(storeent_id,calusage_id,calmethod_id,qtyunit_id,code,description,setccurr,field1).save()
            Calscaleds(calscale_id,language_id,description).save()
            Crulescale(calscale_id,calrule_id).save()
            return {"msg":"Successfully saved calculation scale","calscaledata":Calscale.read(storeent_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error saving calculation scale. Error {0}".format(e.message)},422

class create_taxcalrange(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calmethod_id")
        self.parser.add_argument("calscale_id")
        self.parser.add_argument("cumulative")
        self.parser.add_argument("rangestart")
        self.parser.add_argument("value")
        super(create_taxcalrange,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calmethod_id=data['calmethod_id']
        calscale_id=data['calscale_id']
        cumulative=data['cumulative']
        rangestart=data['rangestart']
        value=float(data['value'])
        try:
            calrange_id=Calrange(calmethod_id,calscale_id,rangestart,cumulative).save()
            Calrlookup(calrange_id,value=value).save()
            return {"msg":"Successfully saved calculation range","calrangedata":Calrange.read()},200
        except EntryException as e:
            return {"msg":"Error saving calculation range. Error: {0}".format(e.message)},422

