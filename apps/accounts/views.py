from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserLogoutSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Registration",
        description="Register a new user with email, username, nationality, and phone",
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise ValidationError(
                "You are already logged in."
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),  
        }, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Login",
        description="Login with email and password to get JWT tokens",
        request=UserLoginSerializer,
        responses={200: UserLoginSerializer},
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise ValidationError(
                "You are already logged in."
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),    
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User Logout",
        description="Logout the current user (requires authentication)",
        request=UserLogoutSerializer,
        responses={204: None},
    )
    def post(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


