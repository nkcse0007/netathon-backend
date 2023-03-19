import logging
from django.contrib.auth.models import BaseUserManager
from utils.constants import *
from utils.common import generate_response

logger = logging.getLogger(__name__)


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return True

    else:
        return False


class ManagerAccountUser(BaseUserManager):
    def create_user(self, input_data, permissions=None, is_verified=False,
                    **kwargs):

        user = self.model(email=self.normalize_email(input_data["email"].lower()), password=input_data["password"])
        user.name = input_data['name'] if 'name' in input_data else input_data["email"].split("@")[0]
        user.phone_code = input_data['phone_code'] if input_data and 'phone_code' in input_data and input_data['phone_code'] else ''
        user.phone = input_data['phone'] if input_data and 'phone' in input_data and input_data['phone'] else ''
        user.is_verified = is_verified

        user.set_password(input_data["password"])
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        logger.info('Creating superuser with email %s', email)
        input_data = {
            "email": email,
            "password": password,
            'name': email.split('@')[0]

        }
        user = self.create_user(input_data, None,  True)

        logger.info('Superuser %s successfully created!', user)

        return user

    def clean(self, *args, **kwargs):
        if not kwargs['email'] or not type(kwargs['email']) == str or not validate_email(kwargs['email']):
            return generate_response(message='Email is missing or invalid.', status=400)
        if not kwargs['password'] or not type(kwargs['password']) == str or not len(kwargs['password']) > 5:
            return generate_response(message='Password is missing or invalid. password should be minimum 6 characters.', status=400)
        return None
