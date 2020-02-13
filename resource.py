from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.authentication.authentication import Plcyacct,Plcypasswd

class default_password_policy(Resource):
    def get(self):return Plcypasswd.readdefault(),200

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
                if userreg_id==users_id:
                    access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                    return {"access_token":access_token,"refresh_token":refresh_token,"msg":"Successfully initialized organization: {0}".format(orgentityname)},200
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
                "refresh_token":refresh_token,"user_id":usersign.member_id,"employer":usersign.employer},200
            else:return {"msg":"Error: Incorrect username or password"},422

