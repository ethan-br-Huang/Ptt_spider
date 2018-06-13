from flask import Blueprint
from . import check_sign, check_logout
from .. import restapi

auth = Blueprint('auth', __name__)
restapi.init_app(auth)
restapi.add_resource(check_sign.checkSign, '/sign')
restapi.add_resource(check_logout.checkLogout, '/logout')
