from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer, LoginUserSerializer, ChangePasswordSerializer
from .models import CustomUser

from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, OpenApiExample
from drf_spectacular.utils import extend_schema, inline_serializer

@extend_schema(
    tags=["Test"],
    summary="Test description of retrieve method",
    responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=None,
            description='Описание 500 ответа'),
    }
)
@api_view(['POST'])
def test(requset):
    return Response({'token': 'token'}, status=status.HTTP_200_OK)

@extend_schema(
    summary="Create user method",
    request=UserSerializer,
    responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_400_BAD_REQUEST: UserSerializer.errors,
    }
)
@api_view(['POST'])
def reg_user(requset):
    if requset.method == 'POST':
        serializer = UserSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Login user method",
    request=LoginUserSerializer,
    responses={
        status.HTTP_200_OK: inline_serializer(
            "Successfully login",
            fields={'token': serializers.CharField()}
        ),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            "Invalid credentials",
            fields={'error': serializers.CharField()}
        ),
    }
)
@api_view(['POST'])
def user_login(requset):
    if requset.method == 'POST':
        username = requset.data.get('email')
        password = requset.data.get('password')

        user = None
        # if '@' in username:
        #     try:
        #         user = CustomUser.objects.get(email=username)
        #     except ObjectDoesNotExist:
        #         pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    summary="Logout user method",
    request=[],
    responses={
        status.HTTP_200_OK: inline_serializer(
            "Successfully loggen out",
            fields={'message': serializers.CharField()}
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: inline_serializer(
            "Server error",
            fields={'error': serializers.CharField()}
        ),
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(requset):
    if requset.method == 'POST':
        try:
            requset.user.auth_token.delete()
            return Response({'message': 'Successfully loggen out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Change password method",
    request=ChangePasswordSerializer,
    responses={
        status.HTTP_200_OK: inline_serializer(
            "Password changed successfully",
            fields={
                'message': serializers.CharField(),
                'new_password': serializers.CharField()
                },
        ),
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            "Incorrect old password",
            fields={'message': serializers.CharField()}
        ),
        status.HTTP_400_BAD_REQUEST: ChangePasswordSerializer.errors
    },
    parameters=[
        OpenApiParameter(
            name='Authorization',
            location=OpenApiParameter.HEADER,
            required=False,
            type=str,
            examples=[
                OpenApiExample(
                    'Token',
                    value='Token 6984592d42dd3a85026bade599eef92893d325d4'
                ),
            ],
        ),
    ]
)
@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new = serializer.data.get('new_password')
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully', 'new_password': str(new)}, status=status.HTTP_200_OK)
            return Response({'message': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)