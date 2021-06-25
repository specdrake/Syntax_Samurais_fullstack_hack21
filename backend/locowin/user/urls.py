from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/',RegisterView.as_view(),name = "register"),
    path('email-verify/',VerifyEmail.as_view(),name = "email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',LoginApiView.as_view(),name = "login"),
    path('check-auth/',CheckAuthView.as_view(),name='check-auth'),
]