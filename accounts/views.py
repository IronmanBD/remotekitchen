from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, LoginSerializer


# Create your views here.
class RegistrationAPI(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"MSG": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token = RefreshToken.for_user(user)

                return Response({"access_token": str(token.access_token), 'refresh_token': str(token), "username": username}, status=status.HTTP_200_OK)
            else:
                return Response({"MSG": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"MSG": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"MSG": "Logout Successfull"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"MSG": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)


