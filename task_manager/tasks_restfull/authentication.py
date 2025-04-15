from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tasks_restfull.models import CustomToken


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