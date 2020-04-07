from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.members.members import ListAllMembers
import json
from ops.mailer.mailer import Mailer

class create_organization(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("membertype",help='compulsory field',required=True)
        self.parser.add_argument("memberstate",help="compulsory field",required=True)
        self.parser.add_argument("orgentitytype",help="compulsory field",required=True)
        self.parser.add_argument("registertype",help="compulsory field",required=True)
        self.parser.add_argument("profiletype",help="compulsory field",required=True)
        self.parser.add_argument("orgentityname",help="compulsory field",required=True)
        self.parser.add_argument("logonid",help="compulsory field",required=True)
        self.parser.add_argument("logonpassword",help="compulsory field",required=True)
        super(create_organization,self).__init__()

    @staticmethod
    def generate_hash(password):return sha256.hash(password)

    def post(self):
        data=self.parser.parse_args()
        membertype=data["membertype"]
        memberstate=data["memberstate"]
        orgentitytype=data["orgentitytype"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        orgentityname=data["orgentityname"]
        logonid=data["logonid"]
        logonpassword=data["logonpassword"]
        try:
            member=Member(membertype,memberstate)
            exists=member.user_exists(logonid)
            if exists:return {"msg":"User {0} already exists. Choose another identity".format(logonid)},200
            elif exists==False:
                member_id=member.save()
                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=logonid).save()
                users_id=Users(orgentity_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=self.generate_hash(logonpassword),passwordcreation=timestamp_now()).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='permission_editor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                usersign=UserSign(logonid)
                RolePermDefaults('roleasnprm.csv',orgentity_id).save()
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                logonis=Userreg.logoniswhat(logonid)
                if logonis=="email":Address(addrbook_id,member_id,orgentityname,email1=logonid).save()
                elif logonis=="phone":Address(addrbook_id,member_id,orgentityname,phone1=logonid).save()
                if userreg_id==users_id:
                    access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                    return {"access_token":access_token,"refresh_token":refresh_token,
                    "msg":"Successfully initialized organization: {0}".format(orgentityname),
                    "user_id":usersign.member_id,"employer":usersign.employer,"roles":usersign.roles,
                    "language_id":usersign.language_id,"profile":usersign.profiletype},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

class login_organization(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("logonid",help="compulsory field",required=True)
        self.parser.add_argument("logonpassword",help="compulsory field",required=True)
        super(login_organization,self).__init__()
    
    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password,hash)
    
    def post(self):
        data=self.parser.parse_args()
        logonid=data["logonid"]
        logonpassword=data["logonpassword"]
        token=Userreg.getpassword(logonid)
        if token==None:return {"msg":"The user you are attempting to log in does not exist"},422
        elif token!=None:
            if self.verify_hash(logonpassword,token):
                usersign=UserSign(logonid)
                access_token=create_access_token(identity=usersign)
                refresh_token=create_refresh_token(identity=usersign)
                return {"msg":"Successfully logged in as {0}".format(logonid),"access_token":access_token,
                "refresh_token":refresh_token,"user_id":usersign.member_id,"employer":usersign.employer,
                "roles":usersign.roles,"language_id":usersign.language_id,"profile":usersign.profiletype},200
            else:return {"msg":"Error: Incorrect username or password"},422

class UserIdentity(Resource):
    @jwt_required
    def get(self):
        current_user=get_jwt_identity()
        useridentity=get_jwt_claims()
        return dict(current_user=current_user,user=useridentity),200

class read_organization(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("logonid",help="compulsory field",required=True)
        super(read_organization,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        logonid=data['logonid']
        try:
            return {"member":Member.readmember(logonid),"orgentity":Orgentity.readorgentity(logonid),
            "users":Users.readusers(logonid),"busprof":Busprof.readbusprof(logonid),
            "userprof":Userprof.readuserprof(logonid),"addrbook":Addrbook.readaddrbook(logonid),
            "address":Address.readaddress(logonid),"userreg":Userreg.readuserreg(logonid)},200
        except EntryException as e:
            return {"msg":"Error reading organization data. Error {0}".format(e.message)},422

class update_orgentity(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orgentity_id",help="required field",required=True)
        self.parser.add_argument("legalid")
        self.parser.add_argument("orgentitytype",help="compulsory field",required=True)
        self.parser.add_argument("orgentityname",help="required field",required=True)
        self.parser.add_argument("taxpayerid")
        self.parser.add_argument("businesscategory")
        self.parser.add_argument("description")
        self.parser.add_argument("adminfirstname")
        self.parser.add_argument("adminmiddlename")
        self.parser.add_argument("adminlastname")
        super(update_orgentity,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orgentity_id=data["orgentity_id"]
        legalid=data["legalid"]
        orgentitytype=data["orgentitytype"]
        orgentityname=data["orgentityname"]
        taxpayerid=data["taxpayerid"]
        businesscategory=data["businesscategory"]
        description=data["description"]
        adminfirstname=data["adminfirstname"]
        adminmiddlename=data["adminmiddlename"]
        adminlastname=data["adminlastname"]
        try:
            Orgentity(orgentity_id,orgentitytype,orgentityname,legalid=legalid,taxpayerid=taxpayerid,
            businesscategory=businesscategory,description=description,adminfirstname=adminfirstname,
            adminmiddlename=adminmiddlename,adminlastname=adminlastname).update()
            return {"msg":"Successfully updated business information"},200
        except EntryException as e:
            return {"Error updating information. Error {0}".format(e.message)},422

class update_address(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("displayname",help="required field",required=True)
        self.parser.add_argument("description")
        self.parser.add_argument("addrbook_id",help="required field",required=True)
        self.parser.add_argument("status")
        self.parser.add_argument("orgname")
        self.parser.add_argument("nickname",help="required field",required=True)
        self.parser.add_argument("isprimary")
        self.parser.add_argument("lastname")
        self.parser.add_argument("persontitle")
        self.parser.add_argument("firstname")
        self.parser.add_argument("middlename")
        self.parser.add_argument("businesstitle")
        self.parser.add_argument("phone1")
        self.parser.add_argument("phone2")
        self.parser.add_argument("address1")
        self.parser.add_argument("city")
        self.parser.add_argument("state")
        self.parser.add_argument("country")
        self.parser.add_argument("zipcode")
        self.parser.add_argument("email1")
        self.parser.add_argument("email2")
        self.parser.add_argument("addresstype")
        self.parser.add_argument("address_id",help="required field",required=True)
        super(update_address,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        address_id=data["address_id"]
        email2=data["email2"]
        email1=data["email1"]
        zipcode=data["zipcode"]
        country=data["country"]
        state=data["state"]
        city=data["city"]
        address1=data["address1"]
        phone2=data["phone2"]
        phone1=data["phone1"]
        businesstitle=data["businesstitle"]
        middlename=data["middlename"]
        firstname=data["firstname"]
        persontitle=data["persontitle"]
        lastname=data["lastname"]
        isprimary=data["isprimary"]
        orgname=data["orgname"]
        nickname=data["nickname"]
        status=data["status"]
        addrbook_id=data["addrbook_id"]
        description=data["description"]
        displayname=data["displayname"]
        member_id=data["member_id"]
        addresstype=data["addresstype"]
        try:
            addrbook_id=Addrbook(member_id,displayname,description=description).update()
            Address(addrbook_id,member_id,nickname,addresstype=addresstype,address_id=address_id,email2=email2,email1=email1,zipcode=zipcode,country=country,
            state=state,city=city,address1=address1,phone2=phone2,businesstitle=businesstitle,phone1=phone1,middlename=middlename,
            firstname=firstname,persontitle=persontitle,lastname=lastname,isprimary=isprimary,status=status).update()
            return {"msg":"Successfully updated contact information"},200
        except EntryException as e:
            return {"msg":"Error updating contact information. Error {0}".format(e.message)},422

class update_preferences(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id")
        self.parser.add_argument("setccurr")
        self.parser.add_argument("description")
        self.parser.add_argument("displayname")
        self.parser.add_argument("preferredcomm")
        self.parser.add_argument("photo")
        self.parser.add_argument("rcvsmsnotification")
        self.parser.add_argument("dn",help="required field",required=True)
        self.parser.add_argument("registertype",help="required field",required=True)
        self.parser.add_argument("profiletype",help="required field",required=True)
        self.parser.add_argument("users_id",help="required field",required=True)
        super(update_preferences,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        users_id=data["users_id"]
        rcvsmsnotification=data["rcvsmsnotification"]
        photo=data["photo"]
        preferredcomm=data["preferredcomm"]
        displayname=data["displayname"]
        description=data["description"]
        setccurr=data["setccurr"]
        dn=data["dn"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        language_id=data["language_id"]
        rcvsms=None
        if rcvsmsnotification=="Yes":data["rcvsms"]=1
        elif rcvsmsnotification=="No":data["rcvsms"]=0
        rcvsms=data["rcvsms"]
        try:
            Users(users_id,registertype,dn=dn,profiletype=profiletype,language_id=language_id,setccurr=setccurr).update()
            # isf=Userprof.isfilled(users_id)
            if Userprof.isfilled(users_id)==0:
                Userprof(users_id,photo=photo,description=description,displayname=displayname,preferredcomm=preferredcomm,rcvsmsnotification=rcvsms).save()
            elif Userprof.isfilled(users_id) != 0:
                Userprof(users_id,photo=photo,description=description,displayname=displayname,preferredcomm=preferredcomm,rcvsmsnotification=rcvsms).update()
            return {"msg":"Successfully updated preference information"},200
        except EntryException as e:
            return {"msg":"Error updating preferences. Error: {0}".format(e.message)},422

class list_all_members(Resource):
    # @jwt_required
    def get(self):return ListAllMembers().data(),200

class list_roles(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required field",required=True)
        super(list_roles,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Role.read_roles(language_id),200

class _create_business_user(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("membertype",help="required field",required=True)
        self.parser.add_argument("memberstate",help="compulsory field",required=True)
        self.parser.add_argument("registertype",help="required field",required=True)
        self.parser.add_argument("profiletype",help="required field",required=True)
        self.parser.add_argument("firstname",help="required field",required=True)
        self.parser.add_argument("middlename",help="required field",required=True)
        self.parser.add_argument("lastname",help="required field",required=True)
        self.parser.add_argument("logonid",help="required field",required=True)
        self.parser.add_argument("logonpassword",help="required field",required=True)
        self.parser.add_argument("employerid",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        super(_create_business_user,self).__init__()

    @staticmethod
    def generate_hash(password):return sha256.hash(password)
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        membertype=data["membertype"]
        memberstate=data["memberstate"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        firstname=data["firstname"]
        middlename=data["middlename"]
        lastname=data["lastname"]
        logonid=data["logonid"]
        logonpassword=data["logonpassword"]
        employerid=data["employerid"]
        member_id=data["member_id"]
        try:
            member_id=Member(membertype,memberstate=memberstate).approve_member(member_id)
            users=Users(member_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registrationupdate=timestamp_now())
            users_id=users.update()
            userreg=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=self.generate_hash(logonpassword),passwordcreation=timestamp_now())
            userreg_id=userreg.update()
            users_id=Busprof(userreg_id,org_id=employerid).update()
            usersign=UserSign(logonid)
            addrbook_id=Addrbook(member_id,firstname+' '+middlename+' '+lastname,description="{}: Address Book".format(firstname+' '+middlename+' '+lastname)).update()
            logonis=Userreg.logoniswhat(logonid)
            address_id=Address.readaddress(member_id)['address_id']
            if logonis=="email":Address(addrbook_id,member_id,logonid,email1=logonid,address_id=address_id).update()
            elif logonis=="phone":Address(addrbook_id,member_id,logonid,phone1=logonid,address_id=address_id).update()
            access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
            return {"msg":"Successfully signed on.","access_token":access_token,"refresh_token":refresh_token},200
        except EntryException as e:
            return {"msg":"Error initializing business user. Error {}".format(e.message)},422

class create_business_user(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("membertype",help="required field",required=True)
        self.parser.add_argument("memberstate",help="compulsory field",required=True)
        self.parser.add_argument("registertype",help="required field",required=True)
        self.parser.add_argument("profiletype",help="required field",required=True)
        self.parser.add_argument("firstname",help="required field",required=True)
        self.parser.add_argument("middlename",help="required field",required=True)
        self.parser.add_argument("lastname",help="required field",required=True)
        self.parser.add_argument("logonid",help="required field",required=True)
        self.parser.add_argument("employerid",help="required field",required=True)
        self.parser.add_argument("role_id",help="required field",required=True)
        super(create_business_user,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        membertype=data["membertype"]
        memberstate=data["memberstate"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        firstname=data["firstname"]
        middlename=data["middlename"]
        lastname=data["lastname"]
        logonid=data["logonid"]
        employerid=data["employerid"]
        role_id=data["role_id"]
        try:
            member=Member(membertype,memberstate=memberstate)
            exists=member.user_exists(logonid)
            if exists:return {"msg":"A user with that identity already exists. Choose another identity"},200
            elif exists==False:
                member_id=member.save()
                users_id=Users(member_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id']).save()
                Mbrrole(member_id,role_id,employerid).save()
                Busprof(users_id,org_id=employerid).save()
                usersign=UserSign(logonid)
                addrbook_id=Addrbook(member_id,firstname+' '+lastname,description="{}: Address Book".format(firstname+' '+lastname)).save()
                logonis=Userreg.logoniswhat(logonid)
                if logonis=="email":
                    Address(addrbook_id,member_id,logonid,email1=logonid).save()
                    if userreg_id==users_id:
                        # send EMail notification
                        access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                        Mailer("pronovserver@gmail.com","jmsoyewale@gmail.com","Pronov Confirmation Email","http://localhost:8080/#/confirmident/"+access_token,"f10aeb05").buildmessage()
                elif logonis=="phone":
                    Address(addrbook_id,member_id,logonid,phone1=logonid,firstname=firstname,middlename=middlename,lastname=lastname).save()
                    # send SMS notification
                return {"usersdata":ListAllMembers().data(),"msg":"Business user will now receive email or SMS notification to proceed."},200
        except EntryException as e:
            return {"msg":"Error initializing business user. Error {}".format(e.message)},422

class append_roles(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("components",action="append")
        super(append_roles,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        components=data['components']
        roles=[json.loads(x.replace("\'", "\"")) for x in components]
        [Mbrrole(v['member_id'],v['role_id'],v['orgentity_id']).save() for v in roles]
        return {"msg":"Saved"},200

class suspend_member(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("action",help="required field",required=True)
        self.parser.add_argument("status",help="required field",required=True)
        super(suspend_member,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        action=data["action"]
        status=data["status"]
        try:
            if status != "Approved":return {"msg":"This member is already pended."},200
            elif status == "Approved":
                Member.suspend_member(member_id)
                return {"usersdata":ListAllMembers().data(),"msg":"Successfully suspended user"},200
        except EntryException as e:
            return {"msg":"Error saving {}".format(e.message)},422        

class approve_member(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("action",help="required field",required=True)
        self.parser.add_argument("status",help="required field",required=True)
        super(approve_member,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        action=data["action"]
        status=data["status"]
        try:
            if status=="Approved":return {"msg":"This member is already approved"},200
            elif status=="Pending Approval":
                Member.approve_member(member_id)
                return {"usersdata":ListAllMembers().data(),"msg":"Successfully approved member"},200
        except EntryException as e:
            return {"msg":"Error saving {}".format(e.message)},422
