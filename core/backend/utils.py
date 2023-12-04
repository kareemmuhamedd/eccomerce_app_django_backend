import datetime
from django.core.mail import EmailMessage
from random import randint
import uuid
from rest_framework.response import Response

from backend.models import Otp, PasswordResetToken, Token
from core.settings import TEMPLATES_BASE_URL
from django.template.loader import get_template


def send_otp(phone):

    otp = randint(100000, 999999)
    validity = datetime.datetime.now() + datetime.timedelta(minutes=10)
    Otp.objects.update_or_create(phone=phone, defaults={
                                 "otp": otp, "verified": False, "validity": validity, })
    print(otp)
    # todo sms api
    return Response('send otp successfully')


def new_token():
    token = uuid.uuid1().hex
    return token


def token_reponse(user):
    token = new_token()
    Token.objects.create(token=token, user=user)

    return Response('token'+token)

def send_password_reset_email(user):
    try:
        # Generate a new token and expiration time
        token = new_token()
        exp_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

        # Create or update the PasswordResetToken object for the user
        token_obj, created = PasswordResetToken.objects.update_or_create(
            user=user,
            defaults={'token': token, 'expiration_time': exp_time}
        )

        # Prepare data for the email template
        email_data = {
            'token': token,
            'email': user.email,
            'base_url': TEMPLATES_BASE_URL,
        }

        # Render the email template
        message = get_template('emails/reset_password.html').render(email_data)

        # Create and send the email
        msg = EmailMessage('Reset Password', message, to=[user.email])
        msg.content_subtype = 'html'
        msg.send()

        return Response('reset_password_email_sent')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        # You may want to log the error or handle it in a more appropriate way.
        return Response('An error occurred while sending the password reset email.')


def send_password_reset_email(user):
    try:
        token = new_token()
        exp_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

        PasswordResetToken.objects.update_or_create(
            user=user, defaults={'user': user, 'token': token, })
        email_data = {
            'token': token,
            'email': user.email,
            'base_url': TEMPLATES_BASE_URL,
        }

        message = get_template('emails/reset_password.html').render(email_data)

        msg = EmailMessage('Reset Password', body=message, to=[user.email,])
        msg.content_subtype = 'html'

        msg.send()
        return Response('reset_password_email_sent')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        # You may want to log the error or handle it in a more appropriate way.
        return Response('An error occurred while sending the password reset email.')
