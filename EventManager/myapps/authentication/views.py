from myapps.authentication.services import create_user, login_user
from rest_framework.response import Response
from utils.common import generate_response
from myapps.models import UserLoginInfo, OrganizationModel, ArtistModel
from utils.http_code import *
from utils.common import get_user_from_token, get_input_data
from utils.jwt.jwt_security import authenticate_login
from rest_framework.views import APIView


class SignUpApi(APIView):

    @staticmethod
    def post(request) -> Response:
        """
        POST response method for creating user.

        :return: JSON object
        """
        input_data = get_input_data(request)
        response, status = create_user(request, input_data)
        return Response(response, status=status)


class EmailLoginApi(APIView):

    @staticmethod
    def post(request) -> Response:
        input_data = get_input_data(request)
        response, status = login_user(request, input_data)
        return Response(response, status=status)
