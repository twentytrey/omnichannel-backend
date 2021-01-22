from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address,ListAllMembers,OTPLogin,get_random_string
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,timesplits
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.mailer.mailer import Mailer
from ops.stores.stores import Storeorgs
from ops.sms.sms import Sms
from ops.helpers.functions import timestamp_now,timestamp_forever,datetimestamp_forever,datetimestamp_now,CurrencyHelper
from ops.stores.stores import Storeent,Storegrp,Storelang,Curlist,Store,Staddress,EntryException,Storeentds,Ffmcenter,Ffmcentds
from ops.calculations.calculations import InstallCalmethods,InstallStencal,Calcode
from ops.accounting.accounting import InstallAccounts, InstallAccountClasses,transaction_types
from ops.filehandlers.filehandlers import InstallCatalogs,InstallCatgroups
from ops.inventory.inventory import Ra,Radetail
from ops.helpers.functions import reversedate

from ops.stores.stores import MDefaultContractOrg
class m_create_store_organization(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("membertype",help='compulsory field',required=True)
        self.parser.add_argument("memberstate",help="compulsory field",required=True)
        self.parser.add_argument("orgentitytype",help="compulsory field",required=True)
        self.parser.add_argument("registertype",help="compulsory field",required=True)
        self.parser.add_argument("profiletype",help="compulsory field",required=True)
        self.parser.add_argument("orgentityname",help="compulsory field",required=True)
        self.parser.add_argument("phone",help="compulsory field",required=True)
        self.parser.add_argument("adminfirstname")
        self.parser.add_argument("adminlastname")
        self.parser.add_argument("address",help="compulsory field",required=True)
        self.parser.add_argument("country",help="compulsory field",required=True)
        self.parser.add_argument("state",help="compulsory field",required=True)
        self.parser.add_argument("city",help="compulsory field",required=True)
        super(m_create_store_organization,self).__init__()

    def post(self):
        data=self.parser.parse_args()
        membertype=data["membertype"]
        memberstate=data["memberstate"]
        orgentitytype=data["orgentitytype"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        orgentityname=data["orgentityname"]
        phone=data["phone"]
        adminfirstname=data["adminfirstname"]
        adminlastname=data["adminlastname"]
        address=data["address"]
        country=data["country"]
        state=data["state"]
        city=data["city"]
        try:
            member=Member(membertype,memberstate=memberstate)
            exists=member.user_exists(phone)
            if exists:return {"status":"ERR","msg":"A customer organization with that phone already exists. User another phone number"},422
            elif exists==False:
                member_id=member.save()

                InstallCatalogs("catalogtemplates.csv",member_id).save()
                InstallCatgroups("categorytemplates.csv",member_id).save()

                InstallAccountClasses('accountclasses.csv',1,member_id).save()
                InstallAccounts("faccount_templates.csv",member_id,1).save()
                [t.save() for t in transaction_types]

                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=phone).save()
                MDefaultContractOrg(member_id)._execute()
                users_id=Users(orgentity_id,registertype,dn=phone,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                salt=get_random_string(6)
                userreg_id=Userreg(users_id,phone,salt=salt,plcyacct_id=Plcyacct.read_default()['plcyacct_id']).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='store_editor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                usersign=UserSign(phone)
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                Address(addrbook_id,member_id,orgentityname,phone1=phone,addresstype='SB',isprimary=1,lastname=adminlastname,firstname=adminfirstname,address1=address,state=state,country=country,city=city,lastcreate=datetimestamp_now(),selfaddress=1).save()
                # send SMS notification
                sms=Sms(phone[1:].replace(" ",""),"Your PronovApp token is: "+salt,sms_from="PronovApp",dnd="2")
                sms_status,sms_message=sms.send()

                #return {"status":"OK","msg":sms_status+" "+sms_message},200

                if sms_status=="success":return {"status":"OK","msg":"You will receive an SMS token to proceed"},200
                else:return {"status":"OK","msg":"Call Pronov to receive your token."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

class otp_login(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("phone",help="required field",required=True)
        super(otp_login,self).__init__()

    def post(self):
        data=self.parser.parse_args()
        phone=data["phone"]
        o=OTPLogin(phone)
        issigned=o.issignedon()
        if issigned[0]==0:
            return {"status":"OK","msg":"Proceed to enter your token"},200
        elif issigned[0]==1:
            newtoken=o._execute()
            if newtoken != None:
                sms=Sms(phone[1:].replace(" ",""),"Your PronovApp token is: "+newtoken,sms_from="PronovApp",dnd="2")
                sms_status,sms_message=sms.send()
                if sms_status=="success":return {"status":"OK","msg":"You will receive an SMS token to proceed"},200
                else:return {"status":"OK","msg":"Call Pronov to receive your token."},200
            else:return {"status":"ERR","msg":"Invalid logon ID"},422

class m_verify_token(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("logonid",help='compulsory field',required=True)
        self.parser.add_argument("otp",help='compulsory field',required=True)
        super(m_verify_token,self).__init__()

    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password,hash)
    
    def post(self):
        data=self.parser.parse_args()
        logonid=data["logonid"]
        otp=data["otp"]
        users_id=Userreg.getusersid(logonid)
        salt=Userreg.getsalt(users_id)
        if salt==otp:
            usersign=UserSign(logonid)
            Member.approve_member(users_id)
            access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
            return {"status":"OK","access_token":access_token,"refresh_token":refresh_token,
                    "msg":"Successfully verified access token",
                    "user_id":usersign.member_id,"employer":usersign.employer,"roles":usersign.roles,
                    "language_id":usersign.language_id,"profile":usersign.profiletype},200
        else:return {"status":"ERR","msg":"Token entered was unrecognizable"},422

from ops.stores.stores import MDefaultContract
class m_create_store(Resource):
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
        self.parser.add_argument("persontitle")
        self.parser.add_argument("photourl")
        super(m_create_store,self).__init__()
    
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

            MDefaultContract(member_id,store_id)._execute()

            InstallCalmethods('calmethods.csv',store_id).save()
            InstallStencal('stencalusg.csv',store_id).save()
            staddress_id_loc=Staddress(nickname,member_id,field1=photourl,address1=address1,city=city,state=state,country=country,
            email1=email1,phone1=phone1,zipcode=zipcode,firstname=firstname,middlename=middlename,lastname=lastname,
            persontitle=persontitle).save()
            Storeentds(language_id,storeent_id,identifier,staddress_id_loc=staddress_id_loc).save()
            ffmcenter_id=Ffmcenter(member_id,name=identifier,inventoryopflags=1).save()
            Ffmcentds(ffmcenter_id,language_id,staddress_id=staddress_id_loc,displayname=identifier).save()
            return {"status":"OK","msg":"Successfully saved store information","allstores":Storeent.readstores(member_id)},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error saving store information. Error {0}".format(e.message)},422

from ops.stores.stores import StoresForMember,VendorsForMember
class stores_for_member(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",required=True,help="required field")
        super(stores_for_member,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        stores=StoresForMember(member_id)._execute()
        vendors=VendorsForMember()._execute()
        return {"status":"OK","stores":stores,"vendors":vendors},200


class create_po(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("vendorname",required=True,help="required field")
        self.parser.add_argument("storename",required=True,help="required field")
        self.parser.add_argument("openindicator",required=True,help="required field")
        self.parser.add_argument("member_id",required=True,help="required field")
        self.parser.add_argument("orderdate")
        self.parser.add_argument("dateclosed")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("createtime")
        self.parser.add_argument("externalid")
        super(create_po,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        vendorname=data["vendorname"]
        storename=data["storename"]
        openindicator=data["openindicator"]
        member_id=data["member_id"]
        orderdate=data["orderdate"]
        dateclosed=data["dateclosed"]
        lastupdate=data["lastupdate"]
        createtime=data["createtime"]
        externalid=data["externalid"]
        try:
            vendor_id=Ra.getvendorid(vendorname)
            store_id=Ra.getstoreid(storename)
            ra_id=Ra(vendor_id,store_id,timestamp_now(),datetimestamp_now(),openindicator,dateclosed=dateclosed,
            lastupdate=datetimestamp_now(),externalid=timesplits()).save()
            openindicator=Ra.open_or_closed(ra_id)
            if openindicator==None or openindicator==0:Ra.close_ra(ra_id)
            return {"status":"OK","msg":"Successfully initialized purchase order","radata":Ra.read(member_id)},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error initializing purchase order. Error: {}".format(e.message)},422

from ops.catalog.catalog import Listprice,Catentry,Itemspc,Catentdesc,AddItemToContract,Catgpenrel
from ops.trading.trading import Tradeposcn
from ops.offers.offers import Offerprice,Offer,Offerdesc
class m_create_catentry(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("salesprice",help="required field",required=True)
        self.parser.add_argument("itemspc_id")
        self.parser.add_argument("catenttype_id")
        self.parser.add_argument("partnumber")
        self.parser.add_argument("mfpartnumber")
        self.parser.add_argument("mfname")
        self.parser.add_argument("currency")
        self.parser.add_argument("listprice")
        self.parser.add_argument("catalog_id")
        self.parser.add_argument("catgroup_id")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("endofservicedate")
        self.parser.add_argument("name")
        self.parser.add_argument("shortdescription")
        self.parser.add_argument("fullimage")
        self.parser.add_argument("available")
        self.parser.add_argument("published")
        self.parser.add_argument("availabilitydate")
        super(m_create_catentry,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        itemspc_id=data["itemspc_id"]
        catenttype_id=data["catenttype_id"]
        partnumber=data["partnumber"]
        mfpartnumber=data["mfpartnumber"]
        mfname=data["mfname"]
        currency=data["currency"]
        listprice=data["listprice"]
        catalog_id=data["catalog_id"]
        catgroup_id=data["catgroup_id"]
        lastupdate=data["lastupdate"]
        endofservicedate=data["endofservicedate"]
        name=data["name"]
        shortdescription=data["shortdescription"]
        fullimage=data["fullimage"]
        available=data["available"]
        published=data["published"]
        availabilitydate=data["availabilitydate"]
        salesprice=data["salesprice"]
        try:
            c=Catentry(member_id,catenttype_id,partnumber,name,itemspc_id=itemspc_id,mfpartnumber=mfpartnumber,mfname=mfname,lastupdate=lastupdate,availabilitydate=availabilitydate,endofservicedate=endofservicedate)
            nameexists=c.name_exists(name,member_id)
            if nameexists:return {"status":"OK","msg":"A product with that name already exists."},200
            elif nameexists==False:
                oldpart=c.initialpart()
                c.partnumber=oldpart
                catentry_id=c.save()
                newpart=c.updatepart(catentry_id,oldpart)
                itemspc_id=Itemspc(member_id,newpart,baseitem_id=catentry_id,lastupdate=timestamp_now()).save()
                c.update_itemspc(itemspc_id,catentry_id)
                Catentdesc(catentry_id,language_id,published,name=name,shortdescription=shortdescription,fullimage=fullimage,availabilitydate=availabilitydate).save()
                if catgroup_id != None and catalog_id != None:Catgpenrel(catgroup_id,catalog_id,catentry_id).save()
                Listprice(catentry_id,currency,listprice).save()

                a=AddItemToContract(catentry_id,member_id,listprice)
                contract_id=a.getcontract()
                if contract_id!=None:
                    tradeposcn_id=a.gettradeposcn(contract_id)
                    offer_id=Offer(tradeposcn_id,catentry_id,published=1,lastupdate=datetimestamp_now()).save()
                    Offerdesc(offer_id,language_id,"Offer Price").save()
                    Offerprice(offer_id,currency,salesprice).save()

                return {"status":"OK","msg":"Successfully saved product item information","entries":Catentry.readcatentry(member_id,language_id),
                "catentryitems":Catentry.read(member_id,language_id)},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error saving item information. Error {0}".format(e.message)},422

class m_update_catentry(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("catentry_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("salesprice",help="required field",required=True)
        self.parser.add_argument("minoq")
        self.parser.add_argument("itemspc_id")
        self.parser.add_argument("catenttype_id")
        self.parser.add_argument("partnumber")
        self.parser.add_argument("mfpartnumber")
        self.parser.add_argument("mfname")
        self.parser.add_argument("currency")
        self.parser.add_argument("listprice")
        self.parser.add_argument("catalog_id")
        self.parser.add_argument("catgroup_id")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("endofservicedate")
        self.parser.add_argument("name")
        self.parser.add_argument("shortdescription")
        self.parser.add_argument("fullimage")
        self.parser.add_argument("available")
        self.parser.add_argument("published")
        self.parser.add_argument("availabilitydate")
        super(m_update_catentry,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        catentry_id=data["catentry_id"]
        language_id=data["language_id"]
        itemspc_id=data["itemspc_id"]
        catenttype_id=data["catenttype_id"]
        partnumber=data["partnumber"]
        mfpartnumber=data["mfpartnumber"]
        mfname=data["mfname"]
        currency=data["currency"]
        listprice=data["listprice"]
        catalog_id=data["catalog_id"]
        catgroup_id=data["catgroup_id"]
        lastupdate=data["lastupdate"]
        endofservicedate=reversedate(data["endofservicedate"])
        name=data["name"]
        shortdescription=data["shortdescription"]
        fullimage=data["fullimage"]
        available=data["available"]
        published=data["published"]
        availabilitydate=data["availabilitydate"]
        minoq=data["minoq"]
        salesprice=data["salesprice"]
        try:
            c=Catentry(member_id,catenttype_id,partnumber,name,itemspc_id=itemspc_id,mfpartnumber=mfpartnumber,
            mfname=mfname,lastupdate=datetimestamp_now(),availabilitydate=availabilitydate,
            endofservicedate=endofservicedate);c.update(catentry_id)
            d=Catentdesc(catentry_id,language_id,published,name,shortdescription,None,None,
            None,fullimage,None,available,availabilitydate);d.update()
            Listprice.update(catentry_id,currency,listprice)
            if catgroup_id != None and catalog_id != None:
                Catgpenrel(catgroup_id,catalog_id,catentry_id,lastupdate=datetimestamp_now()).update()

            a=AddItemToContract(catentry_id,member_id,listprice)
            contract_id=a.getcontract()
            if contract_id!=None:
                tradeposcn_id=a.gettradeposcn(contract_id)
                offer_id=Offer(tradeposcn_id,catentry_id,minimumquantity=minoq,published=1,lastupdate=datetimestamp_now()).save()
                Offerdesc(offer_id,language_id,"Offer Price").save()
                Offerprice(offer_id,currency,salesprice).save()

            return {"status":"OK","msg":"Successfully updated item information"},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422
