import jwt
from django.conf import settings
from django.contrib.auth.models import User


class JWTBackend(object):

    def authenticate(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.DecodeError:
            return None
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return None

        return user if user.is_active else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None