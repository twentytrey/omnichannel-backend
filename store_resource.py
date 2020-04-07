from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.stores.stores import Storeent,Storegrp,Storelang,Curlist,Store,Staddress,EntryException,Storeentds,Ffmcenter,Ffmcentds
from ops.calculations.calculations import InstallCalmethods,InstallStencal

class create_store(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        self.parser.add_argument("setccurr",help="required field",required=True)
        self.parser.add_argument("identifier",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("ownername",help="required field",required=True)
        self.parser.add_argument("nickname")
        self.parser.add_argument("address1",help="required field",required=True)
        self.parser.add_argument("city")
        self.parser.add_argument("state")
        self.parser.add_argument("country")
        self.parser.add_argument("email1")
        self.parser.add_argument("phone1",help="required field",required=True)
        self.parser.add_argument("zipcode")
        self.parser.add_argument("firstname")
        self.parser.add_argument("middlename")
        self.parser.add_argument("lastname")
        self.parser.add_argument("persontitle")
        self.parser.add_argument("photourl")
        super(create_store,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data['member_id']
        stype=data['type']
        setccurr=data['setccurr']
        identifier=data['identifier']
        language_id=data['language_id']
        ownername=data['ownername']
        nickname=data["identifier"]
        address1=data["address1"]
        city=data["city"]
        state=data["state"]
        country=data["country"]
        email1=data["email1"]
        phone1=data["phone1"]
        zipcode=data["zipcode"]
        firstname=data["firstname"]
        middlename=data["middlename"]
        lastname=data["lastname"]
        persontitle=data["persontitle"]
        photourl=data['photourl']
        try:
            storeent_id=Storeent(member_id,stype,identifier,setccurr=setccurr).save()
            storegrp_id=Storegrp(member_id,ownername).save()
            language_id=Storelang(language_id,storeent_id,setccurr=setccurr).save()
            setccurr=Curlist(storeent_id,setccurr).save()
            store_id=Store(storeent_id,storegrp_id,language_id=language_id,inventoryopflag=1,storetype='B2C').save()
            InstallCalmethods('calmethods.csv',store_id).save()
            InstallStencal('stencalusg.csv',store_id).save()
            staddress_id_loc=Staddress(nickname,member_id,field1=photourl,address1=address1,city=city,state=state,country=country,
            email1=email1,phone1=phone1,zipcode=zipcode,firstname=firstname,middlename=middlename,lastname=lastname,
            persontitle=persontitle).save()
            Storeentds(language_id,storeent_id,identifier,staddress_id_loc=staddress_id_loc).save()
            return {"msg":"Successfully saved store information"},200
        except EntryException as e:
            return {"msg":"Error saving store information. Error {0}".format(e.message)},422

class create_host_warehouse(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        self.parser.add_argument("setccurr",help="required field",required=True)
        self.parser.add_argument("identifier",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("ownername",help="required field",required=True)
        self.parser.add_argument("nickname")
        self.parser.add_argument("address1",help="required field",required=True)
        self.parser.add_argument("city")
        self.parser.add_argument("state")
        self.parser.add_argument("country")
        self.parser.add_argument("email1")
        self.parser.add_argument("phone1",help="required field",required=True)
        self.parser.add_argument("zipcode")
        self.parser.add_argument("firstname")
        self.parser.add_argument("middlename")
        self.parser.add_argument("lastname")
        self.parser.add_argument("persontitle")
        self.parser.add_argument("photourl")
        super(create_host_warehouse,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data['member_id']
        stype=data['type']
        setccurr=data['setccurr']
        identifier=data['identifier']
        language_id=data['language_id']
        ownername=data['ownername']
        nickname=data["identifier"]
        address1=data["address1"]
        city=data["city"]
        state=data["state"]
        country=data["country"]
        email1=data["email1"]
        phone1=data["phone1"]
        zipcode=data["zipcode"]
        firstname=data["firstname"]
        middlename=data["middlename"]
        lastname=data["lastname"]
        persontitle=data["persontitle"]
        photourl=data['photourl']
        try:
            storeent_id=Storeent(member_id,stype,identifier,setccurr=setccurr).save()
            storegrp_id=Storegrp(member_id,ownername).save()
            language_id=Storelang(language_id,storeent_id,setccurr=setccurr).save()
            setccurr=Curlist(storeent_id,setccurr).save()
            store_id=Store(storeent_id,storegrp_id,language_id=language_id,inventoryopflag=1,storetype='B2C').save()
            InstallCalmethods('calmethods.csv',store_id).save()
            InstallStencal('stencalusg.csv',store_id).save()
            staddress_id_loc=Staddress(nickname,member_id,field1=photourl,address1=address1,city=city,state=state,country=country,email1=email1,phone1=phone1,zipcode=zipcode,firstname=firstname,middlename=middlename,lastname=lastname,persontitle=persontitle).save()
            Storeentds(language_id,storeent_id,identifier,staddress_id_loc=staddress_id_loc).save()
            ffmcenter_id=Ffmcenter(member_id,name=identifier,inventoryopflags=1).save()
            Ffmcentds(ffmcenter_id,language_id,staddress_id=staddress_id_loc,displayname=identifier).save()
            return {"msg":"Successfully saved host warehouse"},200
        except EntryException as e:
            return {"msg":"Error saving host warehouse. Error {0}".format(e.message)},422

class list_stores(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required",required=True)
        self.parser.add_argument("language_id",help="required",required=True)
        super(list_stores,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        mid=data["member_id"]
        lid=data["language_id"]
        return Storeent.read(mid,lid),200

class read_ffmcenter(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required",required=True)
        super(read_ffmcenter,self).__init__()
    
    @jwt_required
    def post(self):
        member_id=self.parser.parse_args()['member_id']
        return Ffmcenter.read(member_id),200
