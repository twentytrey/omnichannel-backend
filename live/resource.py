from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address,RevokedToken
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.countryandstate.countryandstate import Country,Stateprov
from ops.language.language import Language
from ops.currency.currency import Setcurr

class default_password_policy(Resource):
    def get(self):return Plcypasswd.readdefault(),200

class list_countries(Resource):
    def get(self):return Country.countries(),200

class list_states_for_country(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("countryabbr",help="compulsory field",required=True)
        super(list_states_for_country,self).__init__()
    
    def post(self):
        data=self.parser.parse_args()
        countryabbr=data["countryabbr"]
        return Stateprov.statesforcountry(countryabbr),200

class list_languages(Resource):
    def get(self):return Language.languages(),200

class list_currencies(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required field",required=True)
        super(list_currencies,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Setcurr.listcurrencies(language_id),200

class user_identity(Resource):
    @jwt_required
    def get(self):
        current_user=get_jwt_identity()
        useridentity=get_jwt_claims()
        # decoded=dict(current_user=current_user,user=useridentity)
        usersign=UserSign(current_user)
        if(usersign.member_id==useridentity["user_id"]):return {"status":"OK"},200
        else:return {"status":"ERR","msg":"Unauthorized user. Access denied."},422

class logout_access(Resource):
    @jwt_required
    def post(self):
        jti=get_raw_jwt()['jti']
        try:
            RevokedToken(jti).add()
            return {"msg":"Access token has been revoked"}
        except Exception as e:
            return {"msg":"Error {}".format(str(e))},500

class logout_refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti=get_raw_jwt()['jti']
        try:
            RevokedToken(jti).add()
            return {"msg":"Refresh token has been revoked"},200
        except Exception as e:
            return {"msg":"Error {}".format(str(e))},500

class token_refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        usersign=UserSign(current_user)
        access_token=create_access_token(identity=usersign)
        return {"access_token":access_token}

