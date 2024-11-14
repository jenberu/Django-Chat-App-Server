from django.urls import path,include
from rest_framework import routers
from .views import UserViewSet ,RegisterViewSet,LoginViewSet,RefreshViewSet
router=routers.DefaultRouter()
router.register(r'user',UserViewSet,basename='user')
router.register(r'register', RegisterViewSet,basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'refresh', RefreshViewSet,basename='refresh')
urlpatterns = [
    path('',include(router.urls)),
]