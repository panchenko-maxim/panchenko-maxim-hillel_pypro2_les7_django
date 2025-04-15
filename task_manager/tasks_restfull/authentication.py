from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tasks_restfull.models import CustomToken
import jwt
from django.conf import settings
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            token = token.split(' ')[1]
            custom_token = CustomToken.objects.get(key=token)
        except (CustomToken.DoesNotExist, IndexError):
            raise AuthenticationFailed('Wrong token!')
        if custom_token.is_expired():
            raise AuthenticationFailed("Token is expired")

        return (custom_token.user, custom_token)


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token is expired")
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Wrong token!')
