import secrets
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings
import jwt


def generate_token():
    return secrets.token_hex(20)

def creat_token_for_user(user):
    from tasks_restfull.models import CustomToken
    token = generate_token()
    expires_at = timezone.now() + timedelta(days=settings.TOKEN_TTL.get("days", 0),
                                            minutes=settings.TOKEN_TTL.get("minutes", 0))
    return CustomToken.objects.create(key=token, user=user, expires_at=expires_at)

def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "username": user.email,
        "exp": timezone.now() + timedelta(days=settings.TOKEN_TTL.get("days", 0),
                                            minutes=settings.TOKEN_TTL.get("minutes", 0)),
        "iat": timezone.now(),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")