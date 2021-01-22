from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever,timesplits
from ops.trading.trading import Policy,Policydesc,Policytc,EntryException
from ops.payment.payment import PaymentPolicy,ReadPolicyTc

class create_paymethod_policy(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("description")
        self.parser.add_argument("endtime")
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("policyname",required=True,help="required field")
        self.parser.add_argument("policytype_id",required=True,help="required field")
        self.parser.add_argument("properties")
        self.parser.add_argument("starttime")
        self.parser.add_argument("storeent_id",required=True,help="required field")
        self.parser.add_argument("timecreated")
        self.parser.add_argument("timeupdated")
        super(create_paymethod_policy,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        description=data["description"]
        endtime=data["endtime"]
        language_id=data["language_id"]
        policyname=data["policyname"]
        policytype_id=data["policytype_id"]
        properties=data["properties"]
        starttime=data["starttime"]
        storeent_id=data["storeent_id"]
        timecreated=data["timecreated"]
        timeupdated=data["timeupdated"]
        try:
            policy_id=Policy(policyname,policytype_id,storeent_id,properties,starttime,endtime).save()
            Policydesc(policy_id,language_id,description,timecreated=datetimestamp_now(),timeupdated=datetimestamp_now()).save()
            paymentpolicies=PaymentPolicy(language_id,policytype_id).read()
            return {"msg":"Successfully saved payment method","paymentpolicies":paymentpolicies},200
        except EntryException as e:
            return {"msg":"Error saving payment method. Error: {}".format(e.message)},422

class list_payment_policies(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("policytype_id",required=True,help="required field")
        super(list_payment_policies,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        policytype_id=data["policytype_id"]
        return PaymentPolicy(language_id,policytype_id).read(),200

class read_payment_policy(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("tcsubtype_id",required=True,help="required field")
        self.parser.add_argument("trading_id",required=True,help="required field")
        super(read_payment_policy,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        tcsubtype_id=data["tcsubtype_id"]
        trading_id=data["trading_id"]
        return ReadPolicyTc(trading_id,tcsubtype_id,language_id).get(),200

from ops.payment.payment import SaveReference
class save_reference(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orders_id",help="required field",required=True)
        self.parser.add_argument("transaction_reference",help="required field",required=True)
        super(save_reference,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orders_id=data["orders_id"]
        transaction_reference=data["transaction_reference"]
        try:
            SaveReference(orders_id,transaction_reference).save()
            return {"status":"OK","msg":"Transaction Successful."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422
