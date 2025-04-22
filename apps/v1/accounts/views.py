from rest_framework import generics, permissions, status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer, \
    ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# class LogoutView(APIView):
#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(
#                 {"detail": "Muvaffaqiyatli chiqish amalga oshirildi"},
#                 status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     def get(self, request):
#         return Response({"message": "Change password endpoint. Please use POST."})


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': "You are loggout out"
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['password']):
                return Response({"password": "Noto‘g‘ri joriy parol."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Parol muvaffaqiyatli o‘zgartirildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
