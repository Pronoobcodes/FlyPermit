from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserLogoutSerializer, 
    UserProfileSerializer
)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Registration successful.',
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            }
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Login successful.',
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            }
        }, status=status.HTTP_200_OK)


class UserLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer

    @extend_schema(
        summary="User Logout",
        description="Logout the current user (requires authentication and refresh token)",
        request=UserLogoutSerializer,
        responses={200: None},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)


class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @extend_schema(
        summary="Retrieve Profile",
        description="Get the authenticated user's profile information",
        responses={200: UserProfileSerializer},
    )
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response({
            'success': True,
            'message': 'Profile retrieved.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Profile",
        description="Update the authenticated user's profile details",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    )
    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'message': 'Profile updated successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


