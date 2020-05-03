from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.stores.stores import Storeent,Storegrp,Storelang,Curlist,Store,Staddress,EntryException,Storeentds,Ffmcenter,Ffmcentds
from ops.calculations.calculations import InstallCalmethods,InstallStencal,Calcode
from ops.catalog.catalog import Catalog,Catgroup
from ops.currency.currency import Setcurr
from ops.shipping.shipping import Shipmode
from ops.calculations.calculations import Calcode,Calcodedesc,Calscale,Calscaleds,Calrule,Crulescale,Calrange,Calrlookup

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
        self.parser.add_argument("city",help="required field",required=True)
        self.parser.add_argument("state",help="required field",required=True)
        self.parser.add_argument("country",help="required field",required=True)
        self.parser.add_argument("email1")
        self.parser.add_argument("phone1",help="required field",required=True)
        self.parser.add_argument("zipcode")
        self.parser.add_argument("firstname",help="required field",required=True)
        self.parser.add_argument("middlename")
        self.parser.add_argument("lastname",help="required field",required=True)
        self.parser.add_argument("persontitle",help="required field",required=True)
        self.parser.add_argument("photourl")
        self.parser.add_argument("superowner",help="required field",required=True)
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
        superowner=data["superowner"]
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
            return {"msg":"Successfully saved store information","allstores":Storeent.readstores(superowner)},200
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
        self.parser.add_argument("city",help="required field",required=True)
        self.parser.add_argument("state",help="required field",required=True)
        self.parser.add_argument("country",help="required field",required=True)
        self.parser.add_argument("email1",help="required field",required=True)
        self.parser.add_argument("phone1",help="required field",required=True)
        self.parser.add_argument("zipcode")
        self.parser.add_argument("firstname")
        self.parser.add_argument("middlename")
        self.parser.add_argument("lastname",help="required field",required=True)
        self.parser.add_argument("persontitle",help="required field",required=True)
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
            return {"msg":"Successfully saved host warehouse","your_stores":Storeent.yourstore(member_id)},200
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

class read_stores(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required",required=True)
        super(read_stores,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        return Storeent.readstores(owner_id),200

class your_stores(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required",required=True)
        super(your_stores,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        return Storeent.yourstore(owner_id),200

class get_store_image(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="required field",required=True)
        super(get_store_image,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data["store_id"]
        return Storeent.get_image(store_id),200

class store_utilities(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('member_id',help="required field",required=True)
        self.parser.add_argument('store_id',help="required field",required=True)
        self.parser.add_argument('language_id',help='required field',required=True)
        super(store_utilities,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data['member_id']
        store_id=data['store_id']
        language_id=data['language_id']
        calcodes=Calcode.read(store_id,language_id,[1,2,3])
        catalogs=Catalog.readcatalogs(member_id,language_id)
        shipmodes=Shipmode.read(store_id,language_id)
        [x.update(dict(attached=Catalog.attachedtostore(store_id,x["catalog_id"])))for x in catalogs]
        catgroups=Catgroup.readcatgroups(member_id,language_id)
        [x.update(dict(attached=Catgroup.attachedtostore(store_id,x["catgroup_id"])))for x in catgroups]
        return dict(calcodes=calcodes,catalogs=catalogs,catgroups=catgroups,shipmodes=shipmodes),200

class create_discount(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("calmethod_id",help="required field",required=True)
        self.parser.add_argument("calmethod_id_app",help="required field",required=True)
        self.parser.add_argument("calmethod_id_qfy",help="required field",required=True)
        self.parser.add_argument("calrangecalmethod_id",help="required field",required=True)
        self.parser.add_argument("calrulecalmethod_id",help="required field",required=True)
        self.parser.add_argument("calrulecalmethod_id_qfy",help="required field",required=True)
        self.parser.add_argument("calrulefield2",help="required field",required=True)
        self.parser.add_argument("calruleflags",help="required field",required=True)
        self.parser.add_argument("calscalecalmethod_id",help="required field",required=True)
        self.parser.add_argument("calscalecode",help="required field",required=True)
        self.parser.add_argument("calusage_id",help="required field",required=True)
        self.parser.add_argument("code",help="required field",required=True)
        self.parser.add_argument("cumulative",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("enddate")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("rangestart",help="required field",required=True)
        self.parser.add_argument("startdate")
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("timelimited")
        self.parser.add_argument("value",help="required field",required=True)
        super(create_discount,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        calmethod_id=data['calmethod_id']
        calmethod_id_app=data['calmethod_id_app']
        calmethod_id_qfy=data['calmethod_id_qfy']
        calrangecalmethod_id=data['calrangecalmethod_id']
        calrulecalmethod_id=data['calrulecalmethod_id']
        calrulecalmethod_id_qfy=data['calrulecalmethod_id_qfy']
        calrulefield2=data['calrulefield2']
        calruleflags=data['calruleflags']
        calscalecalmethod_id=data['calscalecalmethod_id']
        calscalecode=data['calscalecode']
        calusage_id=data['calusage_id']
        code=data['code']
        cumulative=data['cumulative']
        description=data['description']
        enddate=data['enddate']
        language_id=data['language_id']
        rangestart=data['rangestart']
        startdate=data['startdate']
        storeent_id=data['storeent_id']
        timelimited=data['timelimited']
        value=data['value']
        try:
            calcode_id=Calcode(code,calusage_id,storeent_id,calmethod_id,calmethod_id_app,calmethod_id_qfy,
                                    lastupdate=timestamp_now(),startdate=startdate,enddate=enddate).save()
            Calcodedesc(calcode_id,language_id,description).save()
            calrule_id=Calrule(calcode_id,calrulecalmethod_id,calrulecalmethod_id_qfy,startdate=startdate,enddate=enddate,
                                                                            field2=calrulefield2,flags=calruleflags).save()
            calscale_id=Calscale(storeent_id,calusage_id,calscalecalmethod_id,code=calscalecode,description=description).save()
            Calscaleds(calscale_id,language_id,description=description).save()
            Crulescale(calscale_id,calrule_id).save()
            calrange_id=Calrange(calrangecalmethod_id,calscale_id=calscale_id,rangestart=rangestart,cumulative=cumulative).save()
            Calrlookup(calrange_id,value=value).save()
            return {"msg":"Successfully saved pricing discount"},200
        except EntryException as e:
            return {"msg":"Error saving pricing discount. Error: {0}".format(e.message)},422

        
