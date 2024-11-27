from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from django.http import Http404
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from rest_framework.pagination import PageNumberPagination
class CustomPagination(PageNumberPagination):
    page_size = 10 
class UserViewSet(viewsets.ModelViewSet):
    http_method_names=('patch','get')
    permission_classes=[AllowAny]
    serializer_class=UserSerializer
    pagination_class=CustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)
    def get_object(self):
        try:
            obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
            return obj
        except Http404:
            raise Http404("User with this public ID does not exist.")
class UserProfileView(APIView)  :
    permission_classes = [IsAuthenticated]
    def get(self,request,pk=None):
       
        try:
            user=request.user
            return Response(UserSerializer(user).data) 
        except User.DoesNotExist:   
            return Response({"detail":"User not found"},status=status.HTTP_404_NOT_FOUND) 
class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            # Validate input data
            serializer.is_valid(raise_exception=True)
            
            # Save the user and generate tokens
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response({
                "user": serializer.data,
                "refresh": res["refresh"],
                "token": res["access"]
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Handle validation errors (e.g., invalid input data)
            return Response({
                "errors": e.detail  # Returns detailed error messages from serializer
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        serializer =self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data,status=status.HTTP_200_OK)   

class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data,status=status.HTTP_200_OK)