from flask import request
from flask_login import login_user, current_user
from .. import db, login_manager
from ..models import userTB
import hashlib
import binascii
import time
from flask_restful import Resource
from ..api_response import getResponse
import regex

verification = regex.compile('[a-zA-Z0-9~!@#$%^&*()_+\=\-\,./?\\\[\]|{}><`]{8,15}')


class checkSign(Resource):
    def get(self):
        return getResponse(status=401)

    def post(self):
        try:
            data = request.json
            if 'password' in data and 'username' in data:
                username = data['username'].strip()
                password = data['password'].strip()
                if not verification.fullmatch(password) or not verification.fullmatch(username):
                    return getResponse(status=400)
                user = userTB.query.filter_by(username=username).one_or_none()
                dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
                hashlib.md5(b"12").hexdigest()
                if user:
                    dk = hashlib.pbkdf2_hmac('sha256',
                                             password.encode('utf-8'),
                                             user.password_salt.encode('utf-8'),
                                             100000)
                    if user.password_hash == binascii.hexlify(dk).decode('utf8'):
                        login_user(user, remember=False, fresh=True)
                        return getResponse(data={'info': 'login ok', "status": 200}, status=200)
                    else:
                        return getResponse(data={'info': 'password error', "status": 401}, status=401)
                else:
                    salt = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
                    dk = hashlib.pbkdf2_hmac('sha256',
                                             password.encode('utf-8'),
                                             salt.encode('utf-8'),
                                             100000)

                    user = userTB(username=username,
                                  password_hash=binascii.hexlify(dk).decode('utf8'),
                                  password_salt=salt)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True, fresh=True)
                    return getResponse(data={'info': 'created ok', "status": 201}, status=201)
            else:
                return getResponse(status=400)
        except Exception as e:
            print(e)
            return getResponse(status=400)


@login_manager.user_loader
def load_user(user_id):
    return userTB.query.get(int(user_id))
