from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerailizer, LoginSerializer
from django.conf import settings
from django.contrib.auth import authenticate
import jwt

# Create your views here.


class RegisterView(GenericAPIView):

    serializer_class = UserSerailizer

    def post(self, request):

        serializer = UserSerailizer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):

        data = request.data

        username = data.get('username', '')

        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user:

            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")

            serializer = UserSerailizer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

        return Response({'details': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
