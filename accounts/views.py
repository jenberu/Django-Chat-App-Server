from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from django.http import Http404
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.views import TokenRefreshView


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
class RegisterViewSet(viewsets.ViewSet):
     serializer_class = RegisterSerializer
     permission_classes=[AllowAny]
     http_method_names=['post']
     #create method is called when the view is accessed via a POST request.
     def create(self,request,*args,**kwargs):
         serializer=self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         #riggers the create method defined in the RegisterSerializer
         user=serializer.save()
         refresh=RefreshToken.for_user(user)
         res={
             "refresh": str(refresh),
             "access": str(refresh.access_token),
         }
         return Response({
             "user":serializer.data,
             "refresh": res["refresh"],
             "token": res["access"]

         },status=status.HTTP_201_CREATED)

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