from rest_framework import generics,status,permissions,views
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Profile
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings  
import jwt , json
from .permissions import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
import os
from rest_framework.generics import UpdateAPIView,ListAPIView,ListCreateAPIView
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())




class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        """
        Endpoint for registering a user 
        """
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relative_link = reverse('email-verify')
        redirect_url = request.GET.get('redirect_url',None)
        absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
        if redirect_url != None:
            absurl += "&redirect_url=" + redirect_url
        email_body = {}
        email_body['username'] = user.username
        email_body['message'] = 'Verify your email'
        email_body['link'] = absurl
        data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Email Confirmation','to_email' : user.email}
        Util.send_email(data)
        return Response({'status' : "OK",'result': user_data},status = status.HTTP_201_CREATED)

algorithm = "HS256"
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        """
        Endpoint for verification of the mail
        """
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url',None)
        if redirect_url is None:
            redirect_url = os.getenv('EMAIL_REDIRECT')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms = [algorithm])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return redirect(redirect_url + '?email=SuccessfullyActivated')
        except jwt.ExpiredSignatureError as identifier:
            return redirect(redirect_url + '?email=ActivationLinkExpired')
        except jwt.exceptions.DecodeError as identifier:
            return redirect(redirect_url + '?email=InvalidToken')

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        """
        Endpoint for logging in a user
        """
        serializer = self.serializer_class(data=request.data,context = {'current_site' : get_current_site(request).domain})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

class CheckAuthView(views.APIView):
    permission_classes = [Authenticated]

    def get(self,request,*args, **kwargs):
        """
        Endpoint for checking if user is authenticated or not by checking if the JWT token is valid or not.
        """
        return Response({'status' : 'OK',"result" : "Token is Valid"},status=status.HTTP_200_OK)


class SendVerificationMail(generics.GenericAPIView):
    serializer_class = SendEmailVerificationSerializer

    def post(self,request,*args, **kwargs):
        """
        Endpoint for sending a verification mail
        """
        email = request.data.get('email',None)
        if email is None:
            return Response({'status' : 'FAILED','error' : 'Email not provided'},status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email = email).exists():
            return Response({'status' : 'FAILED','error' :'The given email does not exist'},status = status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        redirect_url = request.GET.get('redirect_url',None)
        absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
        if redirect_url != None:
            absurl += "&redirect_url=" + redirect_url
        email_body = {}
        email_body['username'] = user.username
        email_body['message'] = 'Verify your email'
        email_body['link'] = absurl
        data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Email Verification','to_email' : user.email}
        Util.send_email(data)
        return Response({'status' : 'OK','result' :'A Verification Email has been sent'},status = status.HTTP_200_OK)


class ProfileGetView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [Authenticated,IsOwner]
    queryset = Profile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)



class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [Authenticated,IsOwner]
    queryset = Profile.objects.all()
    lookup_field = "owner_id__username"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)