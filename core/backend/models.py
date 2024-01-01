from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    fullname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Otp(models.Model):
    phone = models.CharField(max_length=16)
    otp = models.IntegerField()
    validity = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone


class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tokens_set')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class PasswordResetToken(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_reset_tokens_set')
    validity=timezone.now() + timezone.timedelta(days=1)
    def __str__(self):
        return self.user.email
