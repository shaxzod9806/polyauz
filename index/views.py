from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import random
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from index.models import User
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utilities.models import SMS
from utilities.sms import send_sms
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["user_type"] = self.user.user_type
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["user_id"] = self.user.id
        data["is_active"] = self.user.is_active
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(CreateAPIView):
    serializer_class = UserSerializer
    http_method_names = ['post']

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'user_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='The desc'),
        }
    ))
    def post(self, request):
        data = request.data
        random_number = random.randrange(10000, 99999)
        if len(data['password']) < 8:
            return Response({"message": "password must be more than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=make_password(data["password"]),
            user_type=data["user_type"],
            is_active=False,
            activation_code=random_number
        )
        serializer = UserSerializer(user, many=False)
        sms_itself = SMS.objects.create(phone_number=user.username,
                                        text=data["first_name"] + " bu sizning Tasdiqlash kodingiz: " + str(
                                            random_number))
        if not user.is_active:
            send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
        sms_itself.is_sent = 1
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyUser(APIView):
    user_id = openapi.Parameter(
        'user_id',
        in_=openapi.IN_QUERY,
        description='Enter user id to verify the user ',
        type=openapi.TYPE_INTEGER
    )
    verification_code = openapi.Parameter(
        'verification_code',
        in_=openapi.IN_QUERY,
        description='Enter verification_code to verify the user ',
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[user_id, verification_code])
    def post(self, request):
        user_id = request.GET.get("user_id")
        verification_code = request.GET.get("verification_code")
        user_itself = User.objects.get(id=user_id)
        if user_itself.is_active:
            return Response(
                "User is already activated",
                status=status.HTTP_400_BAD_REQUEST
            )
        if int(verification_code) == int(user_itself.activation_code):
            user_itself.is_active = True
            user_itself.save()
            return Response({"details": "User is successfully activated",
                             "is_active": {user_itself.is_active}},
                            status=status.HTTP_200_OK)
        else:
            return Response("Activation code is wrong", status=status.HTTP_400_BAD_REQUEST)
