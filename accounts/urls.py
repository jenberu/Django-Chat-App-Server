from django.urls import path,include
from rest_framework import routers
from .views import UserViewSet ,RegisterViewSet,LoginViewSet,RefreshViewSet,UserProfileView
router=routers.DefaultRouter()
router.register(r'users',UserViewSet,basename='user')
router.register(r'register', RegisterViewSet,basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'token/refresh', RefreshViewSet,basename='refresh')
urlpatterns = [
    path('',include(router.urls)),
    path('user/profile/',UserProfileView.as_view(),name="user_profile"),
]