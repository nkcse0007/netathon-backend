from myapps.models import UserLoginInfo, OrganizationModel, ArtistModel
from utils.common import generate_response
from utils.http_code import *
from utils.constants import *
from utils.jwt.jwt_security import get_access_token
from django.db.models import Q
import random
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)


def create_user(request, input_data):
    errors = UserLoginInfo.objects.clean(**input_data)
    if errors:
        return errors
    user = UserLoginInfo.objects.filter(email=input_data['email'].lower())
    if user:
        return generate_response(
            message='This user is already exist in our record with this email, please login.'
        )
    user = UserLoginInfo.objects.create_user(
        input_data,
        None,
        True,
    )
    access_token = get_access_token(request, user)
    return generate_response({'access_token': access_token,
                                       'logged_in_as': f"{user.email}",
                                       'meta': {
                                           'id': user.id,
                                           'email': user.email,
                                           'phone': user.phone,
                                           'phone_code': user.phone_code,
                                           'role': user.role,
                                       }
                                       }, message='User Created', status=21)


def login_user(request, input_data):
    if 'email' not in input_data or not input_data['email']:
        return generate_response(message='email is missing or invalid.')
    if 'password' not in input_data or not input_data['password']:
        return generate_response(message='password is required.')
    try:
        user = UserLoginInfo.objects.get(
            Q(email=input_data['email'].lower()) | Q(phone=input_data['email']))
    except:
        return generate_response(message='No record found with this email or phone, please signup first.')
    if not check_password(input_data['password'], user.password):
        return generate_response(message='Email or password you provided is invalid. please check it once',
                                 status=401)
    if not user.is_active:
        return generate_response(message='User is blocked by admin, Please contact admin.',
                                 status=401)
    if user.is_deleted:
        return generate_response(message='User has deleted their account previously, please contact admin.',
                                 status=401)
    if not user.is_verified:
        return generate_response(message='User is not verified his account, please check your email.',
                                 status=401)
    else:
        access_token = get_access_token(request, user)
        return generate_response(data={'access_token': access_token,
                                       'logged_in_as': f"{user.email}",
                                       'meta': {
                                           'id': user.id,
                                           'email': user.email,
                                           'phone': user.phone,
                                           'phone_code': user.phone_code,
                                           'role': user.role,
                                       }
                                       }, status=200)
