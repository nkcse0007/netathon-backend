import uuid
import requests
import string
import random
from utils.http_code import *
import os
from datetime import datetime, timedelta, timezone


def get_input_data(request):
    if request.method == 'GET':
        input_data = request.GET
    else:
        input_data = request.data
    return input_data


def generate_response(data=None, message=None, status=400):
    if status == 200 or status == 201:
        status_bool = True
    else:
        status_bool = False

    return {
        'data': data,
        'message': modify_slz_error(message, status_bool),
        'status': status_bool,
    }, status



def modify_slz_error(message, status):
    final_error = list()
    if message:
        if type(message) == str:
            if not status:
                final_error.append(
                    {
                        'error': message
                    }
                )
            else:
                final_error = message
        elif type(message) == list:
            final_error = message
        else:
            for key, value in message.items():
                final_error.append(
                    {'error': str(key) + ': ' + str(value[0])}
                )
    else:
        final_error = None
    return final_error


def get_user_from_token(request=None, token=None):
    from utils.jwt.jwt_security import get_token, JwtAuth
    if not token:
        token = get_token(request)
    Jwt = JwtAuth(token)
    user, headers = Jwt.decode()[0], Jwt.decode()[1]
    return user