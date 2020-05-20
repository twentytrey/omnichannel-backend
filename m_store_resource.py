from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address,ListAllMembers
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.mailer.mailer import Mailer
from ops.stores.stores import Storeorgs
from ops.sms.sms import Sms
from ops.helpers.functions import timestamp_now,timestamp_forever,datetimestamp_forever,datetimestamp_now,CurrencyHelper
from ops.stores.stores import Storeent,Storegrp,Storelang,Curlist,Store,Staddress,EntryException,Storeentds,Ffmcenter,Ffmcentds
from ops.calculations.calculations import InstallCalmethods,InstallStencal,Calcode

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
        self.parser.add_argument("adminfirstname",help="compulsory field",required=True)
        self.parser.add_argument("adminlastname",help="compulsory field",required=True)
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
            if exists:return {"msg":"A customer organization with that identity already exists. Choose another identity"},200
            elif exists==False:
                member_id=member.save()
                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=phone).save()
                users_id=Users(orgentity_id,registertype,dn=phone,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                salt='M{}{}{}{}'.format(member_id,registertype,profiletype,phone[-1])
                userreg_id=Userreg(users_id,phone,salt=salt,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=salt,passwordcreation=None).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='store_editor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                usersign=UserSign(phone)
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                Address(addrbook_id,member_id,orgentityname,phone1=phone,addresstype='SB',isprimary=1,lastname=adminlastname,firstname=adminfirstname,address1=address,state=state,country=country,city=city,lastcreate=datetimestamp_now(),selfaddress=1).save()
                # send SMS notification
                sms=Sms(phone[1:].replace(" ",""),"Your PronovApp token is: "+salt,sms_from="PronovApp",dnd="2")
                sms_status,sms_message=sms.send()

                return {"msg":sms_status+" "+sms_message},200

                # if sms_status=="success":return {"msg":"You will receive an SMS token to proceed"},200
                # else:return {"msg":"Unable to send SMS token to user. Error: {}.".format(sms_message)},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

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
            return {"access_token":access_token,"refresh_token":refresh_token,
                    "msg":"Successful",
                    "user_id":usersign.member_id,"employer":usersign.employer,"roles":usersign.roles,
                    "language_id":usersign.language_id,"profile":usersign.profiletype},200
        else:return {"msg":"Token entered was unrecognizable"},422

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
        self.parser.add_argument("persontitle",help="required field",required=True)
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
            InstallCalmethods('calmethods.csv',store_id).save()
            InstallStencal('stencalusg.csv',store_id).save()
            staddress_id_loc=Staddress(nickname,member_id,field1=photourl,address1=address1,city=city,state=state,country=country,
            email1=email1,phone1=phone1,zipcode=zipcode,firstname=firstname,middlename=middlename,lastname=lastname,
            persontitle=persontitle).save()
            Storeentds(language_id,storeent_id,identifier,staddress_id_loc=staddress_id_loc).save()
            return {"status":"OK","msg":"Successfully saved store information","allstores":Storeent.readstores(member_id)},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error saving store information. Error {0}".format(e.message)},422
