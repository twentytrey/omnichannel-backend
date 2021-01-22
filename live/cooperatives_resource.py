from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever
from ops.members.members import Mbrgrp,Member,EntryException,Users,Userprof,Role,Mbrrole,Busprof,Addrbook,Address,Mbrgrpmbr
from ops.accounting.accounting import InstallAccounts, InstallAccountClasses,transaction_types
from ops.accounting.accounting import Acclass,Acclassdsc,Acclassrel,Accountclassrel,EntryException,Faccount,Faccountdsc,Facctransaction,Transaction,Transactiontype
from ops.coop.coop import CheckMember,FetchMembers

class initialize_cooperative(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("mbrgrpname",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("description")
        self.parser.add_argument("dn")
        self.parser.add_argument("field1")
        self.parser.add_argument("field3")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("country",help="required field",required=True)
        self.parser.add_argument("state",help="required field",required=True)
        self.parser.add_argument("address1",help="required field",required=True)
        super(initialize_cooperative,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        mbrgrpname=data["mbrgrpname"]
        language_id=data["language_id"]
        description=data["description"]
        dn=data["dn"]
        field1=data["field1"]
        field3=data["field3"]
        lastupdate=data["lastupdate"]
        country=data["country"]
        state=data["state"]
        address1=data["address1"]
        try:
            member=Member('G',1)
            exists=member.user_exists(mbrgrpname)
            if exists:
                return {"msg":"A entity with that name already exists. Are you attempting to create another?"},200
            elif exists==False:
                member_id=member.save()
                mbrgrp_id=Mbrgrp(member_id,owner_id,mbrgrpname,description=description,lastupdate=datetimestamp_now()).save()
                
                users_id=Users(member_id,'R',dn=mbrgrpname,profiletype='B',language_id=language_id,registration=datetimestamp_now(),setccurr="NGN",field1=mbrgrpname).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='cooperative'][0]['role_id']
                
                InstallAccountClasses('accountclasses.csv',1,member_id).save()
                InstallAccounts("faccount_templates.csv",member_id,1).save()
                [t.save() for t in transaction_types]

                users_id=Busprof(member_id,org_id=owner_id).save()
                addrbook_id=Addrbook(member_id,mbrgrpname,description="{}: Address Book".format(mbrgrpname)).save()
                Address(addrbook_id,member_id,mbrgrpname,addresstype="SB",address1=address1,state=state,country=country).save()
                coops=Mbrgrp.read(owner_id)
                return {"msg":"Successfully initialized cooperative society.","coops":coops},200
        except EntryException as e:return {"msg":"Error {}".format(e.message)},422

class list_coops(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(list_coops,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        return Mbrgrp.read(owner_id),200

class signup_to_coop(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("mbrgrp_id",help="required field",required=True)
        self.parser.add_argument("transactiontype")
        super(signup_to_coop,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        mbrgrp_id=data["mbrgrp_id"]
        transactiontype=data["transactiontype"]
        ismember=CheckMember(member_id,mbrgrp_id).check()
        if ismember==False:
            try:
                if transactiontype=='TRANSFR':
                    Mbrgrpmbr(member_id,mbrgrp_id,exclude='1').save()
                    return {"status":"OK","msg":"Your membership will be approved once your transfer is confirmed."},200
                elif transactiontype=='DEP' or transactiontype==None:
                    Mbrgrpmbr(member_id,mbrgrp_id).save()
                    return {"status":"OK","msg":"Successfully subscribed to cooperative group."},200
            except EntryException as e:
                return {"status":"ERR","msg":"Error {}".format(e.message)},422
        elif ismember==True:
            return {"status":"OK","msg":"You are already a member of that cooperative"},200

class check_membership(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("mbrgrp_id",help="required field",required=True)
        super(check_membership,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=int(data["member_id"])
        mbrgrp_id=int(data["mbrgrp_id"])
        ismember=CheckMember(member_id,mbrgrp_id).check()
        return {"status":"OK","msg":ismember},200

class list_subs(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("mbrgrp_id")
        super(list_subs,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        mbrgrp_id=data["mbrgrp_id"]
        return Mbrgrpmbr.read(mbrgrp_id),200

from ops.accounting.accounting import ConfirmTransaction
class deposit_contribution(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("amount",help="required field",required=True)
        self.parser.add_argument("transactiontype",help="required field",required=True)
        self.parser.add_argument("memo")
        self.parser.add_argument("setccurr")
        self.parser.add_argument("holder_id")
        self.parser.add_argument("referencenumber",help="required field",required=True)
        super(deposit_contribution,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        amount=data["amount"]
        memo=data["memo"]
        setccurr=data["setccurr"]
        holder_id=data["holder_id"]
        transactiontype=data["transactiontype"]
        referencenumber=data["referencenumber"]
        # TRANSFR,DEP
        try:
            transaction_id=Transaction(transactiontype,holder_id,amount,member_id,datetimestamp_now(),memo=memo).save()
            Facctransaction(transaction_id,Faccount.getid("Investments",member_id),"D").save()
            Facctransaction(transaction_id,Faccount.getid("Cash",member_id),"C").save()
            if transactiontype=="DEP":
                ConfirmTransaction(holder_id,member_id,referencenumber,transaction_id,"Y").save()
                return {"status":"OK","msg":"Transaction successful"},200
            elif transactiontype=="TRANSFR":
                ConfirmTransaction(holder_id,member_id,referencenumber,transaction_id,"N").save()
                return {"status":"OK","msg":"Your contribution will take effect when transfer is confirmed."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error: {}".format(e.message)},422

from ops.members.members import Mbrgrpcond
class save_preferences(Resource):
    def  __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("signupfee",help="required field",required=True)
        self.parser.add_argument("interestrate",help="required field",required=True)
        self.parser.add_argument("profitratio",help="required field",required=True)
        self.parser.add_argument("contribution",help="required field",required=True)
        self.parser.add_argument("coop_id",help="required field",required=True)
        super(save_preferences,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        signupfee=data["signupfee"]
        interestrate=data["interestrate"]
        profitratio=data["profitratio"]
        contribution=data["contribution"]
        coop_id=data["coop_id"]
        try:
            Mbrgrpcond(coop_id,field1="signupfee",field2=signupfee).save()
            Mbrgrpcond(coop_id,field1="interestrate",field2=interestrate).save()
            Mbrgrpcond(coop_id,field1="profitratio",field2=profitratio).save()
            Mbrgrpcond(coop_id,field1="contribution",field2=contribution).save()
            return {"status":"OK","msg":"Successfully saved preferences."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

class update_email(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("user_id",help="required field",required=True)
        self.parser.add_argument("email1",help="required field",required=True)
        super(update_email,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        user_id=data["user_id"]
        email1=data["email1"]
        try:
            Address.updateemail(user_id,email1)
            return {"status":"OK","msg":"Successfully updated email information"},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

class fetch_members(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("mbrgrp_id",help="required field",required=True)
        super(fetch_members,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        mbrgrp_id=data["mbrgrp_id"]
        return FetchMembers(mbrgrp_id).read(),200

from ops.coop.coop import FetchPendingTransactions,ConfirmCTransaction
class fetch_pending_transactions(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("mbrgrp_id",help="required field",required=True)
        super(fetch_pending_transactions,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        mbrgrp_id=data["mbrgrp_id"]
        return FetchPendingTransactions(member_id,mbrgrp_id).read(),200

class confirm_transactions(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("holder_id",required=True,help="required field")
        self.parser.add_argument("payee_id",required=True,help="required field")
        self.parser.add_argument("referencenumber",required=True,help="required field")
        super(confirm_transactions,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        holder_id=data["holder_id"]
        payee_id=data["payee_id"]
        referencenumber=data["referencenumber"]
        try:
            c=ConfirmCTransaction(holder_id,payee_id,referencenumber)
            c.confirm();c.lock_unlock()
            return {"status":"OK","msg":"Successfully confirmed transaction"},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

from ops.coop.loan import CooperativeRules
class cooperative_rules(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(cooperative_rules,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        c=CooperativeRules(member_id,language_id)
        data=c.read();data.update({"symbol":c.symbol})
        group=c.group
        return {"status":"OK","data":data,"group":group},200

from ops.coop.coop import Credit,CreditStatus
class save_credit_request(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("setccurr")
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("mbrgrp_id",help="required field",required=True)
        self.parser.add_argument("timecreated")
        self.parser.add_argument("timeupdated")
        self.parser.add_argument("nextduedate")
        self.parser.add_argument("tenure")
        self.parser.add_argument("rate")
        self.parser.add_argument("creditlimit")
        self.parser.add_argument("decimalfield1")
        self.parser.add_argument("decimalfield2")
        self.parser.add_argument("plan_integration")
        self.parser.add_argument("plan_code")
        self.parser.add_argument("plan_id")
        self.parser.add_argument("customer_code")
        self.parser.add_argument("subscription_code")
        self.parser.add_argument("email_token")
        super(save_credit_request,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        setccurr=data["setccurr"]
        member_id=data["member_id"]
        mbrgrp_id=data["mbrgrp_id"]
        timecreated=datetimestamp_now()
        timeupdated=data["timeupdated"]
        nextduedate=data["nextduedate"]
        tenure=data["tenure"]
        rate=data["rate"]
        creditlimit=data["creditlimit"]
        decimalfield1=data["decimalfield1"]
        decimalfield2=data["decimalfield2"]
        plan_integration=data["plan_integration"]
        plan_code=data["plan_code"]
        plan_id=data["plan_id"]
        customer_code=data["customer_code"]
        subscription_code=data["subscription_code"]
        email_token=data["email_token"]
        outstandingc=Credit.outstanding(member_id)
        if outstandingc==True:
            return {"status":"OK","msg":"Sorry, you must clear out your outstanding loan before obtaining another"},200
        elif outstandingc==False:
            try:
                credit_id=Credit(member_id,mbrgrp_id,tenure,rate,setccurr,timecreated,timeupdated,nextduedate,creditlimit,
                decimalfield1,decimalfield2,plan_integration,plan_code,plan_id,customer_code,subscription_code,email_token).save()
                CreditStatus(credit_id).save()
                return {"status":"OK","msg":"Successfully saved credit request","credit_id":credit_id},200
            except EntryException as e:
                return {"status":"ERR","msg":"Error {}".format(e.message)},422

from ops.coop.coop import Guarantor
from ops.accounting.accounting import Transaction,Facctransaction
class save_guarantor(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("guarantor_id",help="required field",required=True)
        self.parser.add_argument("borrower_id",help="required field",required=True)
        self.parser.add_argument("credit_id",help="required field",required=True)
        self.parser.add_argument("amount")
        self.parser.add_argument("mbrgrp_id")
        super(save_guarantor,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        guarantor_id=data["guarantor_id"]
        borrower_id=data["borrower_id"]
        credit_id=data["credit_id"]
        amount=data["amount"]
        mbrgrp_id=data["mbrgrp_id"]
        try:
            Guarantor(guarantor_id,borrower_id,credit_id).save()
            return {"status":"OK","msg":"Successfully requested guarantor."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

class delete_guarantor(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("guarantor_id",help="required field",required=True)
        self.parser.add_argument("borrower_id",help="required field",required=True)
        self.parser.add_argument("credit_id",help="required field",required=True)
        self.parser.add_argument("amount")
        self.parser.add_argument("mbrgrp_id")
        super(delete_guarantor,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        guarantor_id=data["guarantor_id"]
        borrower_id=data["borrower_id"]
        credit_id=data["credit_id"]
        amount=data["amount"]
        mbrgrp_id=data["mbrgrp_id"]
        try:
            Guarantor(guarantor_id,borrower_id,credit_id).delete()
            return {"status":"OK","msg":"Successfully withdrawn guarantor."},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

from ops.coop.loan import TransactionHistory
class read_transaction_history(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_transaction_history,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        return {"status":"OK","data":TransactionHistory(member_id,language_id).read()},200

from ops.coop.loan import LoanHistory
class loan_history(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(loan_history,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        data=LoanHistory(member_id,language_id).read()
        return {"status":"OK","data":data},200

from ops.coop.loan import GuarantorView
class guarantor_view(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        super(guarantor_view,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        data=GuarantorView(member_id).get()
        return {"status":"OK","data":data},200

from ops.coop.loan import GuarantorBalance
class cash_balance(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(cash_balance,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        g=GuarantorBalance(member_id,language_id)
        b=g.balanceval;b_format=g.balanceval_fmt;s=g.symbol
        return {"status":"OK","balance":b,"symbol":s,"format":b_format},200

from ops.coop.loan import Guarantees
class guarantees(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("guarantor_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(guarantees,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        guarantor_id=data["guarantor_id"]
        language_id=data["language_id"]
        d=Guarantees(guarantor_id,language_id).read()
        return d,200
