import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class Register(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        jwtPayload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(jwtPayload, 'secret', algorithm='HS256')  # TODO Store the secret properly
        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {
            "token": token
        }
        return response


class CurrentUser(APIView):

    def get(self, request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])  # TODO fetch from Stored the secret properly
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
