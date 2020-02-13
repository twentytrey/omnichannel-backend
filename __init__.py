from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import RevokedTokenError
from flask_cors import CORS
import os,datetime
from logging import Formatter,FileHandler
from werkzeug.utils import secure_filename
import config
from ops.members.members import RevokedToken

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
@app.before_first_request
def initializedefaults():
    ld=LanguageDefault('langdefaults.csv')
    if ld.isfilled:pass
    elif ld.isfilled==False:ld.save()
    cd=CurrencyDefaults('allcurrencycodes.csv')
    if cd.isfilled:pass
    elif cd.isfilled==False:cd.save()
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

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def banstatus(decryptedtoken):
    jti=decryptedtoken['jti']
    r=RevokedToken(jti)
    return r.isbanned()

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
def hello():
    return "ProNov RESTful API Server"

import resource
api.add_resource(resource.default_password_policy,"/api/v1.0/default_password_policy",endpoint="default_password_policy")
api.add_resource(resource.create_organization,"/api/v1.0/create_organization",endpoint="create_organization")
api.add_resource(resource.login_organization,"/api/v1.0/login_organization",endpoint="login_organization")

if __name__=='__main__':
    app.run(threaded=True)
