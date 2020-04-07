from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.accounting.accounting import Acclass,Acclassdsc,Acclassrel,Accountclassrel,EntryException,Faccount,Faccountdsc,Facctransaction,Transaction,Transactiontype
import json

class list_accounts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required")
        self.parser.add_argument("member_id",required=True,help="required")
        super(list_accounts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data['language_id']
        member_id=data['member_id']
        return Faccount.read(member_id,language_id),200

class list_acclasses(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required")
        self.parser.add_argument("member_id",required=True,help="required")
        super(list_acclasses,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data['language_id']
        member_id=data['member_id']
        return Acclass.read(member_id,language_id),200

class create_account(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("accountnumber",required=True,help="required")
        self.parser.add_argument("identifier",required=True,help="required")
        self.parser.add_argument("routingnumber")
        self.parser.add_argument("setccurr")
        self.parser.add_argument("description")
        self.parser.add_argument("acclass_id",required=True,help="required")
        self.parser.add_argument("balance")
        self.parser.add_argument("timecreated")
        self.parser.add_argument("member_id",required=True,help="required")
        self.parser.add_argument("language_id",required=True,help="required")
        super(create_account,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        accountnumber=data["accountnumber"]
        identifier=data["identifier"]
        routingnumber=data["routingnumber"]
        setccurr=data["setccurr"]
        description=data["description"]
        acclass_id=data["acclass_id"]
        balance=data["balance"]
        timecreated=data["timecreated"]
        member_id=data["member_id"]
        language_id=data["language_id"]
        try:
            faccount_id=Faccount(accountnumber,identifier,member_id,routingnumber,setccurr).save()
            Faccountdsc(faccount_id,language_id,description).save()
            Accountclassrel(acclass_id,faccount_id).save()
            return {"msg":"Successfully created account","accountsdata":Faccount.read(member_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error creating account. Error {0}".format(e.message)},422