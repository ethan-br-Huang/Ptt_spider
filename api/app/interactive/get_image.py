from flask_restful import Resource
from flask_login import login_required, current_user
from ..models import pictureTB
from .. import db
from ..api_response import getResponse
from flask import request


class getImage(Resource):
    @login_required
    def get(self, user_id=None, image_number=100):
        try:
            if "getuser" in str(request.url_rule) and user_id:
                images = pictureTB\
                    .query\
                    .add_columns(pictureTB.data)\
                    .filter_by(author_id=user_id)\
                    .all()
                return getResponse(data=[i.data for i in images], status=200)
            else:
                images = pictureTB\
                    .query\
                    .add_columns(pictureTB.data)\
                    .order_by(pictureTB.id.desc())\
                    .limit(image_number)\
                    .all()
                return getResponse(data=[i.data for i in images], status=200)
        except Exception as e:
            print(e)
            return getResponse(status=400)
