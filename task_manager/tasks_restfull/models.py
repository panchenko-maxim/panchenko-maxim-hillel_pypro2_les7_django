from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class CustomToken(models.Model):
    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token for {self.user.email}"

