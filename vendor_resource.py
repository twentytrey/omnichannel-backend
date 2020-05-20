from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.members.members import Member,Orgentity,Users,Userreg,Mbrrole,Busprof,EntryException,Role,UserSign,Userprof,Address,RolePermDefaults,Addrbook,Address,ListAllMembers
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever,timesplits
from ops.authentication.authentication import Plcyacct,Plcypasswd
from ops.vendor.vendor import Vendor,Vendordesc
from ops.inventory.inventory import Ra,Radetail,Receipt,ReceiveInventory
from ops.fulfillment.fulfillment import Inventory
from ops.catalog.catalog import Listprice


class create_vendor_organization(Resource):
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
        super(create_vendor_organization,self).__init__()

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
            if exists:return {"msg":"A Vendor with that identity already exists. Choose another identity"},200
            elif exists==False:
                member_id=member.save()
                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=logonid).save()
                users_id=Users(orgentity_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=self.generate_hash(logonpassword),passwordcreation=timestamp_now()).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='vendor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                usersign=UserSign(logonid)
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                logonis=Userreg.logoniswhat(logonid)
                if logonis=="email":Address(addrbook_id,member_id,orgentityname,email1=logonid).save()
                elif logonis=="phone":Address(addrbook_id,member_id,orgentityname,phone1=logonid).save()
                # if userreg_id==users_id:
                #     access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                #     return {"access_token":access_token,"refresh_token":refresh_token,"msg":"Successfully initialized organization: {0}".format(orgentityname)},200
                return {"msg":"Vendor organization will now receive email and SMS on instructions to proceed"},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

class _create_vendor_organization(Resource):
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
        self.parser.add_argument("language_id",help="compulsory field",required=True)
        super(_create_vendor_organization,self).__init__()

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
        language_id=data["language_id"]
        try:
            member=Member(membertype,memberstate)
            exists=member.user_exists(logonid)
            if exists:return {"msg":"A Vendor with that identity already exists. Choose another identity"},200
            elif exists==False:
                member_id=member.save()
                orgentity_id=Orgentity(member_id,orgentitytype,orgentityname,dn=logonid).save()
                users_id=Users(orgentity_id,registertype,dn=logonid,profiletype=profiletype,language_id=defaultlanguage(),registration=timestamp_now()).save()
                userreg_id=Userreg(users_id,logonid,plcyacct_id=Plcyacct.read_default()['plcyacct_id'],logonpassword=logonpassword,passwordcreation=None).save()
                roles=Role.read_roles(defaultlanguage());rid=[x for x in roles if x['name']=='vendor'][0]['role_id']
                Mbrrole(userreg_id,rid,orgentity_id).save()
                users_id=Busprof(member_id,org_id=orgentity_id).save()
                vendor_id=Vendor(users_id,lastupdate=timestamp_now(),vendorname=orgentityname).save()
                Vendordesc(vendor_id,language_id,orgentityname,timestamp_now())
                usersign=UserSign(logonid)
                addrbook_id=Addrbook(member_id,orgentityname,description="{}: Address Book".format(orgentityname)).save()
                Address(addrbook_id,member_id,orgentityname,phone1=logonid).save()
                # logonis=Userreg.logoniswhat(logonid);
                # if logonis=="email":Address(addrbook_id,member_id,orgentityname,email1=logonid).save()
                # elif logonis=="phone":Address(addrbook_id,member_id,orgentityname,phone1=logonid).save()
                # if userreg_id==users_id:
                #     access_token=create_access_token(identity=usersign);refresh_token=create_refresh_token(identity=usersign)
                #     return {"access_token":access_token,"refresh_token":refresh_token,"msg":"Successfully initialized organization: {0}".format(orgentityname)},200
                return {"usersdata":ListAllMembers().data(),"msg":"Successfully Saved Vendor Information"},200
        except EntryException as e:
            return {"msg":"Error initializing organization {0}. Error {1}".format(orgentityname,e.message)},422

class list_vendors(Resource):
    @jwt_required
    def get(self):
        return {"vendors":Vendor.read(),"lastraid":Ra.lastraid()},200

class create_ra(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("vendor_id",required=True,help="required field")
        self.parser.add_argument("store_id",required=True,help="required field")
        self.parser.add_argument("orderdate")
        self.parser.add_argument("openindicator",required=True,help="required field")
        self.parser.add_argument("dateclosed")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("createtime")
        self.parser.add_argument("externalid",required=True,help="required field")
        super(create_ra,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        vendor_id=data["vendor_id"]
        store_id=data["store_id"]
        orderdate=data["orderdate"]
        openindicator=data["openindicator"]
        dateclosed=data["dateclosed"]
        lastupdate=data["lastupdate"]
        createtime=data["createtime"]
        externalid=data["externalid"]
        try:
            ra_id=Ra(vendor_id,store_id,timestamp_now(),datetimestamp_now(),openindicator,dateclosed=dateclosed,
            lastupdate=datetimestamp_now(),externalid=timesplits()).save()
            openindicator=Ra.open_or_closed(ra_id)
            if openindicator==None or openindicator==0:Ra.close_ra(ra_id)
            return {"msg":"Successfully initialized purchase order","radata":Ra.read()},200
        except EntryException as e:
            return {"msg":"Error initializing purchase order. Error: {}".format(e.message)},422

class read_ra(Resource):
    @jwt_required
    def get(self):return Ra.read(),200

class get_ra(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("ra_id",help="required field",required=True)
        super(get_ra,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        ra_id=data["ra_id"]
        return Ra.read_ra(ra_id),200

class read_ra_detail(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("ra_id",help="required field",required=True)
        super(read_ra_detail,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        ra_id=data["ra_id"]
        return Radetail.read(ra_id),200

class create_radetail(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catentry_id",help="required field",required=True)
        self.parser.add_argument("cost")#add on qtyreceived
        self.parser.add_argument("expecteddate",help="required field",required=True)
        self.parser.add_argument("ffmcenter_id",help="required field",required=True)
        self.parser.add_argument("itemspc_id",help="required field",required=True)
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("qtyallocated",help="required field",required=True)
        self.parser.add_argument("qtyordered",help="required field",required=True)
        self.parser.add_argument("qtyreceived",help="required field",required=True)
        self.parser.add_argument("qtyremaining",help="required field",required=True)
        self.parser.add_argument("ra_id",help="required field",required=True)
        self.parser.add_argument("radetailcomment",help="required field",required=True)
        self.parser.add_argument("setccurr")#add on qtyreceived
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("vendor_id",help="required field",required=True)#add
        super(create_radetail,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        catentry_id=data["catentry_id"]
        expecteddate=data["expecteddate"]
        ffmcenter_id=data["ffmcenter_id"]
        itemspc_id=data["itemspc_id"]
        lastupdate=data["lastupdate"]
        qtyallocated=data["qtyallocated"]
        qtyordered=data["qtyordered"]
        qtyreceived=data["qtyreceived"]
        qtyremaining=data["qtyremaining"]
        ra_id=data["ra_id"]
        radetailcomment=data["radetailcomment"]
        store_id=data["store_id"]
        cost=data["cost"]
        vendor_id=data["vendor_id"]
        setccurr=data["setccurr"]
        try:
            radetail_id=Radetail(ra_id,itemspc_id,expecteddate,ffmcenter_id,qtyordered,qtyreceived,
                qtyremaining,qtyallocated,radetailcomment,datetimestamp_now()).save()
            detailsitems=Radetail.read(ra_id)
            qtyonhand=Receipt.getqtyonhand(catentry_id,ffmcenter_id,store_id)
            Receipt(catentry_id,store_id,ffmcenter_id,datetimestamp_now(),datetimestamp_now(),cost=cost,
                comment1=radetailcomment,lastupdate=datetimestamp_now(),receipttype="EIR",qtyreceived=qtyreceived,
                qtyonhand=qtyonhand,vendor_id=vendor_id,setccurr=setccurr,radetail_id=radetail_id).save()
            if cost!=None:Listprice.update(catentry_id,setccurr,cost)
            Inventory(catentry_id,ffmcenter_id,store_id,qtyreceived).save()
            openindicator=Ra.open_or_closed(ra_id)
            if openindicator==None or openindicator==0:Ra.close_ra(ra_id)
            elif openindicator > 0:Ra.open_ra(ra_id)
            indicator=Ra.getindicator(ra_id)
            return {"msg":"Successfully saved purchase order details.",
            "indicator":indicator,"detailsitems":detailsitems},200
        except EntryException as e:
            return {"msg":"Error {}".format(e.message)},422

class read_receipts(Resource):
    @jwt_required
    def get(self):return Receipt.read(),200

class receive_inventory(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("radetail_id",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        super(receive_inventory,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        radetail_id=data["radetail_id"]
        store_id=data["store_id"]
        return ReceiveInventory(radetail_id,store_id).data,200

class inventory_receipt(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catentry",help="required field",required=True)
        self.parser.add_argument("comment1",help="required field",required=True)
        self.parser.add_argument("cost",help="required field",required=True)
        self.parser.add_argument("createtime",help="required field",required=True)
        self.parser.add_argument("currency",help="required field",required=True)
        self.parser.add_argument("ffmcenter_id",help="required field",required=True)
        self.parser.add_argument("lastupdate",help="required field",required=True)
        self.parser.add_argument("qtyinkits",help="required field",required=True)
        self.parser.add_argument("qtyinprocess",help="required field",required=True)
        self.parser.add_argument("qtyonhand",help="required field",required=True)
        self.parser.add_argument("qtyreceived",help="required field",required=True)
        self.parser.add_argument("radetail_id",help="required field",required=True)
        self.parser.add_argument("receiptdate",help="required field",required=True)
        self.parser.add_argument("receipttype",help="required field",required=True)
        self.parser.add_argument("rtnrcptdsp_id")
        self.parser.add_argument("setccurr",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("vendor_id",help="required field",required=True)
        self.parser.add_argument("versionspc_id",help="required field",required=True)
        self.parser.add_argument("ra_id",help="required field",required=True)
        super(inventory_receipt,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        catentry=data["catentry"]
        comment1=data["comment1"]
        cost=data["cost"]
        createtime=data["createtime"]
        currency=data["currency"]
        ffmcenter_id=data["ffmcenter_id"]
        lastupdate=data["lastupdate"]
        qtyinkits=int(data["qtyinkits"])
        qtyinprocess=int(data["qtyinprocess"])
        qtyonhand=int(data["qtyonhand"])
        qtyreceived=int(data["qtyreceived"])
        radetail_id=data["radetail_id"]
        receiptdate=data["receiptdate"]
        receipttype=data["receipttype"]
        rtnrcptdsp_id=data["rtnrcptdsp_id"]
        setccurr=data["setccurr"]
        store_id=data["store_id"]
        vendor_id=data["vendor_id"]
        versionspc_id=data["versionspc_id"]
        ra_id=data["ra_id"]
        try:
            Radetail.update(qtyreceived,datetimestamp_now(),radetail_id)
            qtyonhand=Inventory.update(qtyreceived,versionspc_id,ffmcenter_id,store_id)
            detailsitems=Radetail.read(ra_id)
            receipt_id=Receipt(versionspc_id,store_id,ffmcenter_id,receiptdate,datetimestamp_now(),cost,comment1,None,
                datetimestamp_now(),receipttype,qtyreceived,qtyinprocess,qtyonhand=qtyonhand,qtyinkits=qtyinkits,
                vendor_id=vendor_id,setccurr=setccurr,radetail_id=radetail_id,rtnrcptdsp_id=rtnrcptdsp_id).save()
            openindicator=Ra.open_or_closed(ra_id)
            if openindicator==None or openindicator==0:Ra.close_ra(ra_id)
            elif openindicator > 0:Ra.open_ra(ra_id)
            indicator=Ra.getindicator(ra_id)
            return {"msg":"Successfully received inventory item","indicator":indicator,"detailsitems":detailsitems},200
        except EntryException as e:
            return {"msg":"Error receiving inventory item. Error {}".format(e.message)},422

class list_inventory(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required field",required=True)
        super(list_inventory,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Inventory.read(language_id),200
