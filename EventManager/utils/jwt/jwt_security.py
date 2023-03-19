from functools import wraps

import jwt
from datetime import datetime, timedelta
from uuid import uuid4
from myapps.models import UserLoginInfo
from utils.common import generate_response
from utils.http_code import *
import os
from django.http.response import JsonResponse
from utils.common import get_input_data

private_key = open('utils/jwt/private.pem').read()
public_key = open('utils/jwt/public.pub').read()
refresh_private_key = open('utils/jwt/refresh_private.pem').read()
refresh_public_key = open('utils/jwt/refresh_public.pub').read()


class JwtAuth:

    def __init__(self, row_or_token=None):
        self.data = row_or_token

    def encode(self, payload, request, user):
        jwt_id = uuid4().hex
        try:
            origin = request.META['HTTP_ORIGIN'].split('//')[1]
            print(request.META['HTTP_ORIGIN'].split('//')[1])
        except:
            print('EXCEPTION IN ORIGIN>>')
            # print(e)
            origin = ''

        encoded_jwt = jwt.encode(payload,
                                 private_key, algorithm='RS512', headers={
                                    'exp': (datetime.now() + timedelta(days=15)).timestamp(),
                                    'aud': origin,
                                    'sub': user.email,
                                    'iss': 'CommonDashboard',
                                    'kid': jwt_id,
                                    'iat': int(datetime.now().timestamp())
            })

        return encoded_jwt

    def decode(self):
        """
        usage: decode token and find payload and header from the token.
        """
        payload = jwt.decode(self.data, public_key, algorithms='RS512')
        headers = jwt.get_unverified_header(self.data)
        return payload, headers


def authenticate_login(fun):
    """
    param: function
    usage: decorator to check if user is authenticated, token is valid, token not expired.
    """

    @wraps(fun)
    def function_wrapper(request, *args, **kwargs):
        try:
            try:
                token = request.headers.get('Authorization').split()
                if not token:
                    token = get_input_data(request)['access_token']
                if not token:
                    return JsonResponse(generate_response(message='Unauthorised User', status=401))

                if len(token) == 1:
                    return JsonResponse(generate_response(message='Invalid token header, no token provided.',
                                             status=401))

                try:
                    token = token[-1]
                    if token == "null" or not token:
                        return JsonResponse(generate_response(message='Null token not allowed.', status=401))
                except UnicodeError:
                    return JsonResponse(generate_response(
                        message='Error! Invalid token header. Token string should not contain invalid characters.',
                        status=401))

                try:
                    dec = JwtAuth(str(token))
                    payload, headers = dec.decode()
                except UnicodeError:
                    return JsonResponse(generate_response(
                        message='Error! Invalid token header.',
                        status=401))
            except Exception as e:
                print(e)
                return JsonResponse(generate_response(message='Unauthorised user', status=401))

            if datetime.fromtimestamp(headers['exp']) < datetime.now():
                return JsonResponse(generate_response(message='Token Expired.', status=401))

            if UserLoginInfo.objects(id=payload['id']):

                if not UserLoginInfo.objects(id=payload['id']):
                    return JsonResponse(generate_response(message='Unauthorised user', status=401))

                if not UserLoginInfo.objects.get(id=payload['id'])['is_active']:
                    return JsonResponse(generate_response(message='User is inactive. Please contact admin.',
                                             status=401))

                if UserLoginInfo.objects.get(id=payload['id'])['is_deleted']:
                    return JsonResponse(generate_response(message='User is deleted previously. Please contact admin.',
                                             status=401))

                return fun(*args, **kwargs)

            else:
                return JsonResponse(generate_response(message='User is inactive. Please contact admin.',
                                         status=401))

        except Exception as e:
            print(e)
            return JsonResponse(generate_response(message='Authentication failed, Invalid token. Please login again.',
                                     status=401))

    return function_wrapper


def get_token(request):
    """
    param: request
    usage: find token from the request. if token in body, param or header.
    """
    token = request.headers.get('Authorization').split()
    if not token:
        token = get_input_data(request)['access_token']
    if not token:
        return JsonResponse(generate_response(message='Unauthorised User', status=401))

    if len(token) == 1:
        return JsonResponse(generate_response(message='Invalid token header, no token provided.',
                                              status=401))

    token = token[-1]
    if token == "null" or not token:
        return JsonResponse(generate_response(message='Null token not allowed.', status=401))
    return token


def get_user_from_token(request):
    token = get_token(request)
    Jwt = JwtAuth(token)
    user_id, headers = Jwt.decode()[0]['id'] if 'id' in Jwt.decode()[0] else '', Jwt.decode()[1]
    user = UserLoginInfo.objects.get(id=user_id)
    return user, headers


def get_access_token(request, user):
    Jwt = JwtAuth(os.environ.get('VERIFY_TOKEN'))
    response = {
        'id': str(user.id),
        'phone': user.phone,
        'email': user.email,
        'role': user.role,
    }
    return Jwt.encode(response, request, user)
