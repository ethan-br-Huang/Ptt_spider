from flask import Response
import json


def getResponse(data=None, status=200, mimetype='application/json'):
    http_response = {
        400: {'info': "Bad Request", "status": 400},
        422: {'info': "Unprocessable Entity", "status": 422},
        202: {'info': 'Accepted', "status": 202},
        401: {'info': 'Unauthorized', "status": 401},
        404: {'info': "Not Found", "status": 404}
    }
    if data or data == []:
        return Response(json.dumps(data), mimetype=mimetype, status=status)
    else:
        return Response(json.dumps(http_response[status]), mimetype=mimetype, status=status)
