from flask_restful import Resource
from flask_login import login_required, current_user
from ..models import pictureTB
from .. import db
from ..api_response import getResponse
from flask import request


class putImage(Resource):
    @login_required
    def put(self):
        try:
            data = request.json
            if len(data) > 0:
                objects = []
                for d in data:
                    objects += [pictureTB(author_id=current_user.id, data=d)]
                db.session.bulk_save_objects(objects)
                db.session.commit()
                return getResponse(data={'info': 'created ok', "status": 201}, status=201)
        except Exception as e:
            print(e)
            return getResponse(status=400)
