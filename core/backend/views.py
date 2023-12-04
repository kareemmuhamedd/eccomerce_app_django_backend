import datetime
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.models import Otp, User
from backend.utils import send_otp, send_password_reset_email, token_reponse
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password



@api_view(['POST'])
def request_otp(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    if email and phone:
        if User.objects.filter(email=email).exists():
            return Response('email already exists', status=400)
        if User.objects.filter(phone=phone).exists():
            return Response('phone already exists', status=400)
        return send_otp(phone)
    else:
        return Response('data_missing', status=400)


@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')
    otp_obj = get_object_or_404(Otp, phone=phone, verified=False)
    if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
        if otp_obj.otp == otp:
            otp_obj.verified = True
            otp_obj.save()
            return Response('otp_verified_successfully')
        else:
            return Response('Incorrect otp', status=400)
    else:
        return Response('otp exipred', status=400)


@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    fullname = request.data.get('fullname')

    if email and phone and password and fullname:
        otp_obj = get_object_or_404(Otp, phone=phone, verified=True)
        otp_obj.delete()

        User.objects.create(email=email, phone=phone,
                            password=make_password(password), fullname=fullname)
        return Response('account created_successfully')
    else:
        return Response('data_missing', status=400)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')

    if email:
        user = get_object_or_404(User, email=email)
    elif phone:
        user = get_object_or_404(User, phone, phone)
    else:
        return Response('data_missing', status=400)

    if check_password(password, user.password):
        # todo login
        return token_reponse(user)
    else:
        return Response('incorrect password', status=400)
    

@api_view(['POST'])
def password_reset_email(request):
    email = request.data.get('email')
    if not email:
        return Response('params_missing',status=400)
    
    user = get_object_or_404(User,email=email)
    return send_password_reset_email(user)


@api_view(['GET'])
def password_reset_from(request):
    return HttpResponse('')
