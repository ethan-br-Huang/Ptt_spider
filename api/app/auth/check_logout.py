from flask_login import login_required, logout_user, current_user
from flask_restful import Resource
from ..api_response import getResponse


class checkLogout(Resource):
    @login_required
    def get(self):
        username = str(current_user.username)
        logout_user()
        return getResponse(data={'info': f'{username} is Logout ok', "status": 200}, status=200)
