from flask import Flask,jsonify,request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import RevokedTokenError
from flask_cors import CORS
import os,datetime
from logging import Formatter,FileHandler
from werkzeug.utils import secure_filename
import config
from ops.members.members import RevokedToken,EntryException
from ops.helpers.functions import regularize


class ErrorFriendlyApi(Api):
    def error_router(self,original_handler,e):
        if type(e) is ExpiredSignatureError:return original_handler(e)
        elif type(e) is RevokedTokenError:return original_handler(e)
        else:return super(ErrorFriendlyApi,self).error_router(original_handler,e)

app=Flask(__name__)
CORS(app)
api=ErrorFriendlyApi(app)

basedir = os.path.abspath(os.path.dirname(__file__))
logtarget=os.path.join(basedir,"logs/")
if not os.path.isdir(logtarget):os.mkdir(logtarget)
handler=FileHandler(os.path.join(logtarget,"log.txt"),encoding="utf8")
handler.setFormatter(Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"))

app.config.from_object(config.Config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

from ops.language.language import LanguageDefault
from ops.currency.currency import CurrencyDefaults
from ops.currency.currency import NumberUsageDefaults
from ops.authentication.authentication import DefaultPasswordPolicy
from ops.authentication.authentication import DefaultLockoutPolicy
from ops.authentication.authentication import DefaultAccountPolicy
from ops.members.members import RoleDefaults
from ops.countryandstate.countryandstate import CountryDefaults
from ops.countryandstate.countryandstate import StateprovDefaults
from ops.catalog.catalog import CatenttypeDefaults,AttrtypeDefaults,CatreltypeDefaults
from ops.calculations.calculations import CalusageDefaults
from ops.tax.tax import InstallTaxtype
from ops.accounting.accounting import InstallAccountClasses
from ops.trading.trading import InstallPartroles,InstallAttachusg,InstallTctypes

@app.before_first_request
def initializedefaults():
    ld=LanguageDefault('langdefaults.csv')
    if ld.isfilled():pass
    elif ld.isfilled()==False:ld.save()
    cd=CurrencyDefaults('allcurrencycodes.csv')
    if cd.isfilled():pass
    elif cd.isfilled()==False:cd.save()
    nd=NumberUsageDefaults('numberusage.csv')
    if nd.isfilled():pass
    elif nd.isfilled()==False:nd.save()
    dpp=DefaultPasswordPolicy('defaultpasswordpolicy.csv')
    if dpp.isfilled():pass
    elif dpp.isfilled()==False:dpp.save()
    dlp=DefaultLockoutPolicy('defaultlockoutpolicy.csv')
    if dlp.isfilled():pass
    elif dlp.isfilled()==False:dlp.save()
    dap=DefaultAccountPolicy()
    if dap.isfilled():pass
    elif dap.isfilled()==False:dap.savedescription()
    rd=RoleDefaults('rolesdescriptions.csv')
    if rd.isfilled():pass
    elif rd.isfilled()==False:rd.save()
    cd=CountryDefaults('countrycodes.csv')
    if cd.isfilled():pass
    elif cd.isfilled()==False:cd.save()
    sd=StateprovDefaults('ngstatecodes.csv','NG')
    if sd.isfilled():pass
    elif sd.isfilled()==False:sd.save()
    c=CatenttypeDefaults()
    if c.isfilled():pass
    elif c.isfilled()==False:c.save()
    a=AttrtypeDefaults()
    if a.isfilled():pass
    elif a.isfilled()==False:a.enter()
    c=CatreltypeDefaults()
    if c.isfilled():pass
    elif c.isfilled()==False:c.enter()
    cd=CalusageDefaults()
    if cd.isfilled()==True:pass
    elif cd.isfilled()==False:cd.save()
    i=InstallTaxtype('taxtypes.csv')
    if i.isfilled()==True:pass
    elif i.isfilled()==False:i.save()
    i=InstallAccountClasses('accountclasses.csv',1,1)
    if i.isfilled():pass
    elif i.isfilled()==False:i.save()
    i=InstallPartroles('partroles.csv')
    if i.isfilled()==True:pass
    elif i.isfilled()==False:i.save()
    i=InstallAttachusg('attachusg.csv')
    if i.isfilled()==True:pass
    elif i.isfilled()==False:i.save()
    i=InstallTctypes('tctypes.csv')
    if i.isfilled()==True:pass
    elif i.isfilled()==False:i.save()

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def banstatus(decryptedtoken):
    jti=decryptedtoken['jti']
    r=RevokedToken(jti)
    try:
        return r.isbanned()
    except EntryException as e:
        return jsonify({"status":422,"msg":"Error checking token status"}),422

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"status":401,"msg":"access token expired"}),401

@jwt.user_claims_loader
def add_claims_to_token(user):
    return {'roles':user.roles,'user_id':user.member_id,'employer':user.employer,
    'language':user.language_id,'profile':user.profiletype}

@jwt.user_identity_loader
def user_identity_loader(user):
    return user.logonid

@app.route("/")
def hello():return "ProNov RESTful API Server"

@app.route("/profileuploads",methods=["POST","GET"])
def uploads():
    if request.method=='POST':
        files=request.files["image"]
        if files and allowed_file(files.filename):
            filename = secure_filename( files.filename.split('.')[0]+'.'+files.filename.split('.')[-1] )
            app.logger.info("Filename: "+filename)
            updir=os.path.join(basedir,"static/profileuploads/")
            files.save(os.path.join(updir,filename))
            file_size = os.path.getsize(os.path.join(updir,filename))
            file_url="static/profileuploads/"+filename
            return jsonify(url=regularize(file_url),name=filename,size=file_size)

@app.route("/productuploads",methods=["POST","GET"])
def productuploads():
    if request.method=='POST':
        files=request.files["image"]
        if files and allowed_file(files.filename):
            filename = secure_filename( files.filename.split('.')[0]+'.'+files.filename.split('.')[-1] )
            app.logger.info("Filename: "+filename)
            updir=os.path.join(basedir,"static/productuploads/")
            files.save(os.path.join(updir,filename))
            file_size = os.path.getsize(os.path.join(updir,filename))
            file_url="static/productuploads/"+filename
            return jsonify(url=regularize(file_url),name=filename,size=file_size)


import resource,members_resource,catalog_resource,currency_resource,customer_resource,vendor_resource,store_resource,tax_resource,calculation_resource,shipping_resource,accounting_resource
api.add_resource(resource.default_password_policy,"/api/v1.0/default_password_policy",endpoint="default_password_policy")
api.add_resource(members_resource.create_organization,"/api/v1.0/create_organization",endpoint="create_organization")
api.add_resource(members_resource.login_organization,"/api/v1.0/login_organization",endpoint="login_organization")
api.add_resource(members_resource.UserIdentity,"/api/v1.0/useridentity",endpoint="useridentity")
api.add_resource(resource.list_countries,"/api/v1.0/list_countries",endpoint="list_countries")
api.add_resource(resource.list_states_for_country,"/api/v1.0/list_states_for_country",endpoint="list_states_for_country")
api.add_resource(resource.list_languages,"/api/v1.0/list_languages",endpoint="list_languages")
api.add_resource(resource.list_currencies,"/api/v1.0/list_currencies",endpoint="list_currencies")
api.add_resource(members_resource.read_organization,"/api/v1.0/read_organization",endpoint="read_organization")
api.add_resource(members_resource.update_orgentity,"/api/v1.0/update_orgentity",endpoint="update_orgentity")
api.add_resource(members_resource.update_address,"/api/v1.0/update_address",endpoint="update_address")
api.add_resource(members_resource.update_preferences,"/api/v1.0/update_preferences",endpoint="update_preferences")
api.add_resource(catalog_resource.create_catalog,"/api/v1.0/create_catalog",endpoint="create_catalog")
api.add_resource(catalog_resource.read_catalogs,"/api/v1.0/read_catalogs",endpoint="read_catalogs")
api.add_resource(catalog_resource.create_category,"/api/v1.0/create_category",endpoint="create_category")
api.add_resource(catalog_resource.read_categories,"/api/v1.0/read_categories",endpoint="read_categories")
api.add_resource(currency_resource.list_currs,"/api/v1.0/list_currs",endpoint="list_currs")
api.add_resource(catalog_resource.catgroups_for_catalog,"/api/v1.0/catgroups_for_catalog",endpoint="catgroups_for_catalog")
api.add_resource(catalog_resource.create_catentry,"/api/v1.0/create_catentry",endpoint="create_catentry")
api.add_resource(catalog_resource.list_catentries,"/api/v1.0/list_catentries",endpoint="list_catentries")
api.add_resource(catalog_resource.create_composite,"/api/v1.0/create_composite",endpoint="create_composite")
api.add_resource(customer_resource.create_customer_organization,"/api/v1.0/create_customer_organization",endpoint="create_customer_organization")
api.add_resource(customer_resource._create_customer_organization,"/api/v1.0/_create_customer_organization",endpoint="_create_customer_organization")
api.add_resource(vendor_resource.create_vendor_organization,"/api/v1.0/create_vendor_organization",endpoint="create_vendor_organization")
api.add_resource(vendor_resource._create_vendor_organization,"/api/v1.0/_create_vendor_organization",endpoint="_create_vendor_organization")
api.add_resource(members_resource.list_all_members,"/api/v1.0/list_all_members",endpoint="list_all_members")
api.add_resource(members_resource.list_roles,"/api/v1.0/list_roles",endpoint="list_roles")
api.add_resource(members_resource.create_business_user,"/api/v1.0/create_business_user",endpoint="create_business_user")
api.add_resource(members_resource._create_business_user,"/api/v1.0/_create_business_user",endpoint="_create_business_user")
api.add_resource(members_resource.append_roles,"/api/v1.0/append_roles",endpoint="append_roles")
api.add_resource(members_resource.approve_member,"/api/v1.0/approve_member",endpoint="approve_member")
api.add_resource(members_resource.suspend_member,"/api/v1.0/suspend_member",endpoint="suspend_member")
api.add_resource(resource.user_identity,"/api/v1.0/user_identity",endpoint="user_identity")
api.add_resource(store_resource.create_store,"/api/v1.0/create_store",endpoint="create_store")
api.add_resource(store_resource.read_ffmcenter,"/api/v1.0/read_ffmcenter",endpoint="read_ffmcenter")
api.add_resource(store_resource.create_host_warehouse,"/api/v1.0/create_host_warehouse",endpoint="create_host_warehouse")
api.add_resource(tax_resource.read_jurst,"/api/v1.0/read_jurst",endpoint="read_jurst")
api.add_resource(tax_resource.read_jurstgroup,"/api/v1.0/read_jurstgroup",endpoint="read_jurstgroup")
api.add_resource(store_resource.list_stores,"/api/v1.0/list_stores",endpoint="list_stores")
api.add_resource(tax_resource.create_jurstgroup,"/api/v1.0/create_jurstgroup",endpoint="create_jurstgroup")
api.add_resource(tax_resource.create_jurst,"/api/v1.0/create_jurst",endpoint="create_jurst")
api.add_resource(tax_resource.read_taxtype,"/api/v1.0/read_taxtype",endpoint="read_taxtype")
api.add_resource(tax_resource.read_taxcgry,"/api/v1.0/read_taxcgry",endpoint="read_taxcgry")
api.add_resource(tax_resource.create_taxcgry,"/api/v1.0/create_taxcgry",endpoint="create_taxcgry")
api.add_resource(tax_resource.read_calcode,"/api/v1.0/read_calcode",endpoint="read_calcode")
api.add_resource(calculation_resource.read_calcodes,"/api/v1.0/read_calcodes",endpoint="read_calcodes")
api.add_resource(calculation_resource.read_calmethods,"/api/v1.0/read_calmethods",endpoint="read_calmethods")
api.add_resource(tax_resource.create_tax_calcode,"/api/v1.0/create_tax_calcode",endpoint="create_tax_calcode")
api.add_resource(tax_resource.read_taxcalrule,"/api/v1.0/read_taxcalrule",endpoint="read_taxcalrule")
api.add_resource(calculation_resource.methods_from_taxcat,"/api/v1.0/methods_from_taxcat",endpoint="methods_from_taxcat")
api.add_resource(tax_resource.create_taxcalrule,"/api/v1.0/create_taxcalrule",endpoint="create_taxcalrule")
api.add_resource(calculation_resource.read_calscale,"/api/v1.0/read_calscale",endpoint="read_calscale")
api.add_resource(tax_resource.create_taxcalscale,"/api/v1.0/create_taxcalscale",endpoint="create_taxcalscale")
api.add_resource(calculation_resource.read_calrange,"/api/v1.0/read_calrange",endpoint="read_calrange")
api.add_resource(calculation_resource.methods_from_calscale,"/api/v1.0/methods_from_calscale",endpoint="methods_from_calscale")
api.add_resource(tax_resource.create_taxcalrange,"/api/v1.0/create_taxcalrange",endpoint="create_taxcalrange")
api.add_resource(calculation_resource.read_calusage,"/api/v1.0/read_calusage",endpoint="read_calusage")
api.add_resource(shipping_resource.create_shpcalrule,"/api/v1.0/create_shpcalrule",endpoint="create_shpcalrule")
api.add_resource(shipping_resource.read_shpcalrule,"/api/v1.0/read_shpcalrule",endpoint="read_shpcalrule")
api.add_resource(shipping_resource.methods_from_calcode,"/api/v1.0/methods_from_calcode",endpoint="methods_from_calcode")
api.add_resource(accounting_resource.list_accounts,"/api/v1.0/list_accounts",endpoint="list_accounts")
api.add_resource(accounting_resource.list_acclasses,"/api/v1.0/list_acclasses",endpoint="list_acclasses")
api.add_resource(accounting_resource.create_account,"/api/v1.0/create_account",endpoint="create_account")




























































if __name__=='__main__':
    app.run(threaded=True)
