from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/',RegisterView.as_view(),name = "register"),
    path('email-verify/',VerifyEmail.as_view(),name = "email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',LoginApiView.as_view(),name = "login"),
    path('check-auth/',CheckAuthView.as_view(),name='check-auth'),
    path('send-email/',SendVerificationMail.as_view(),name='send-email'),
    path('profile/',ProfileGetView.as_view(),name = "profile"),
    path('profile/<str:owner_id__username>',ProfileUpdateView.as_view(),name = "profile"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'), 
    path('password-change/',ChangePassword.as_view(),name='password-change'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
]