from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever
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

class update_account(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("faccount_id",required=True,help="required")
        self.parser.add_argument("acclass_id",required=True,help="required")
        self.parser.add_argument("accountnumber",required=True,help="required")
        self.parser.add_argument("balance")
        self.parser.add_argument("description")
        self.parser.add_argument("identifier",required=True,help="required")
        self.parser.add_argument("language_id",required=True,help="required")
        self.parser.add_argument("member_id",required=True,help="required")
        self.parser.add_argument("routingnumber")
        self.parser.add_argument("setccurr")
        self.parser.add_argument("timecreated")
        self.parser.add_argument("memo")
        super(update_account,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        faccount_id=data["faccount_id"]
        acclass_id=data["acclass_id"]
        accountnumber=data["accountnumber"]
        balance=float(data["balance"])
        description=data["description"]
        identifier=data["identifier"]
        language_id=data["language_id"]
        member_id=data["member_id"]
        routingnumber=data["routingnumber"]
        setccurr=data["setccurr"]
        memo=data["memo"]
        timecreated=data["timecreated"]
        if balance > 0:
            try:
                Faccount(accountnumber,identifier,member_id,routingnumber,setccurr).update(faccount_id)
                Faccountdsc(faccount_id,language_id,description).update()
                Accountclassrel(acclass_id,faccount_id).update()
                transaction_id=Transaction("GENJNRL",member_id,balance,datetimestamp_now(),None,memo).save()
                cname=Acclass.get_class_name(acclass_id)
                if cname=="Asset":
                    Facctransaction(transaction_id,faccount_id,"D").save()
                    Facctransaction(transaction_id,Faccount.getid("Common Stock",member_id),"C").save()
                return {"msg":"Successfully updated account","accountsdata":Faccount.read(member_id,language_id)},200
            except EntryException as e:
                return {"msg":"Error updating account. Error {0}".format(e.message)},422
        elif balance <= 0:
            try:
                Faccount(accountnumber,identifier,member_id,routingnumber,setccurr).update(faccount_id)
                Faccountdsc(faccount_id,language_id,description).update()
                Accountclassrel(acclass_id,faccount_id).update()
                return {"msg":"Successfully updated account","accountsdata":Faccount.read(member_id,language_id)},200
            except EntryException as e:
                return {"msg":"Error updating account. Error {0}".format(e.message)},422

class create_account(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("acclass_id",required=True,help="required")
        self.parser.add_argument("accountnumber",required=True,help="required")
        self.parser.add_argument("balance")
        self.parser.add_argument("description")
        self.parser.add_argument("identifier",required=True,help="required")
        self.parser.add_argument("language_id",required=True,help="required")
        self.parser.add_argument("member_id",required=True,help="required")
        self.parser.add_argument("routingnumber")
        self.parser.add_argument("setccurr")
        self.parser.add_argument("timecreated")
        self.parser.add_argument("memo")
        super(create_account,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        acclass_id=data["acclass_id"]
        accountnumber=data["accountnumber"]
        balance=data["balance"]
        if balance !="" and balance!=None:balance=float(data["balance"])
        else: balance=0
        description=data["description"]
        identifier=data["identifier"]
        language_id=data["language_id"]
        member_id=data["member_id"]
        routingnumber=data["routingnumber"]
        setccurr=data["setccurr"]
        memo=data["memo"]
        timecreated=data["timecreated"]
        if balance > 0:
            try:
                faccount_id=Faccount(accountnumber,identifier,member_id,routingnumber,setccurr).save()
                Faccountdsc(faccount_id,language_id,description).save()
                Accountclassrel(acclass_id,faccount_id).save()
                transaction_id=Transaction("GENJNRL",member_id,balance,member_id,datetimestamp_now(),None,memo).save()
                cname=Acclass.get_class_name(acclass_id)
                if cname=="Asset":
                    Facctransaction(transaction_id,faccount_id,"D").save()
                    Facctransaction(transaction_id,Faccount.getid("Common Stock",member_id),"C").save()
                return {"msg":"Successfully created account","accountsdata":Faccount.read(member_id,language_id)},200
            except EntryException as e:
                return {"msg":"Error creating account {}".format(e.message)},422
        elif balance <= 0:
            try:
                faccount_id=Faccount(accountnumber,identifier,member_id,routingnumber,setccurr).save()
                Faccountdsc(faccount_id,language_id,description).save()
                Accountclassrel(acclass_id,faccount_id).save()
                return {"msg":"Successfully created account","accountsdata":Faccount.read(member_id,language_id)},200
            except EntryException as e:
                return {"msg":"Error creating account. Error {0}".format(e.message)},422

class ac_read_account(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("faccount_id",help="required field",required=True)
        super(ac_read_account,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        faccount_id=data["faccount_id"]
        return Faccount.readaccount(faccount_id,member_id,language_id),200

class read_transactions(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("faccount_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_transactions,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        faccount_id=data["faccount_id"]
        member_id=data["member_id"]
        language_id=data["language_id"]
        return Faccount.readtransactions(faccount_id,member_id,language_id),200

class credit_cash(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("amount",help="required field",required=True)
        self.parser.add_argument("memo",help="required field",required=True)
        super(credit_cash,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        amount=data["amount"]
        memo=data["memo"]
        try:
            transaction_id=Transaction("GENJNRL",owner_id,amount,datetimestamp_now(),None,memo).save()
            Facctransaction(transaction_id,Faccount.getid("Cash",owner_id),"D").save()
            Facctransaction(transaction_id,Faccount.getid("Common Stock",owner_id),"C").save()
            return {"status":"OK","msg":"Successfully credited account"},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422
