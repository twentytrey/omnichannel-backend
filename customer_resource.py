from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address,ListAllMembers
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.mailer.mailer import Mailer

class create_customer_organization(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("membertype",help='compulsory field',required=True)
        self.parser.add_argument("memberstate",help="compulsory field",required=True)
        self.parser.add_argument("orgentitytype",help="compulsory field",required=True)
        self.parser.add_argument("registertype",help="compulsory field",required=True)
        self.parser.add_argument("profiletype",help="compulsory field",required=True)
        self.parser.add_argument("orgentityname",help="compulsory field",required=True)
        self.parser.add_argument("logonid",help="compulsory field",required=True)
        self.parser.add_argument("logonpassword",help="compulsory field",required=True)
        super(create_customer_organization,self).__init__()

    @staticmethod
    def generate_hash(password):return sha256.hash(password)

    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        membertype=data["membertype"]
        memberstate=data["memberstate"]
        orgentitytype=data["orgentitytype"]
        registertype=data["registertype"]
        profiletype=data["profiletype"]
        orgentityname=data["orgentityname"]
        logonid=data["logonid"]
        logonpassword=data["logonpassword"]
        try:
            member_id=Member(membertype,memberstate=memberstate).approve_member(member_id)
            orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=logonid).update()
            users_id=Users(orgentity_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registrationupdate=timestamp_now()).update()
            userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=self.generate_hash(logonpassword),passwordcreation=timestamp_now()).update()
            users_id=Busprof(member_id,org_id=orgentity_id).update()
            usersign=UserSign(logonid)
            addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).update()
            logonis=Userreg.logoniswhat(logonid)
            address_id=Address.readaddress(member_id)['address_id']
            if logonis=="email":Address(addrbook_id,member_id,orgentityname,email1=logonid,address_id=address_id).update()
            elif logonis=="phone":Address(addrbook_id,member_id,orgentityname,phone1=logonid,address_id=address_id).update()
            access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
            return {"access_token":access_token,"refresh_token":refresh_token,"msg":"Successfully initialized customer organization: {0}".format(orgentityname)},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

class _create_customer_organization(Resource):
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
        super(_create_customer_organization,self).__init__()

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
            member=Member(membertype,memberstate=memberstate)
            exists=member.user_exists(logonid)
            if exists:return {"msg":"A customer organization with that identity already exists. Choose another identity"},200
            elif exists==False:
                member_id=member.save()
                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=logonid).save()
                users_id=Users(orgentity_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=logonpassword,passwordcreation=None).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='store_editor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                usersign=UserSign(logonid)
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                logonis=Userreg.logoniswhat(logonid)
                if logonis=="email":
                    Address(addrbook_id,member_id,orgentityname,email1=logonid).save()
                    if userreg_id==users_id:
                        # send EMail notification
                        access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                        Mailer("pronovserver@gmail.com","jmsoyewale@gmail.com","Pronov Confirmation Email","http://localhost:8080/#/customersignup/"+access_token,"f10aeb05").buildmessage()
                elif logonis=="phone":
                    Address(addrbook_id,member_id,orgentityname,phone1=logonid).save()
                    # send SMS notification
                return {"usersdata":ListAllMembers().data(),"msg":"Customer organization will now receive email and SMS on instructions to proceed"},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422