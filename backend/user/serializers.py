from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import User,Profile,Aadhar
from .exception import *
import re
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .utils import Util
from django.utils.encoding import smart_bytes,smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']
         
    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        # if not username.isalnum():
        #     raise ValidationException("The username should only contain alphanumeric characters")
        if re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{1,75}(?<![-._])$',username) is None:
            raise ValidationException("Username is invalid")
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)
    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,read_only=True)
    password = serializers.CharField(max_length = 68,min_length = 6,write_only=True)
    username = serializers.CharField(max_length = 100)
    tokens = serializers.SerializerMethodField()
    first_time_login = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    def get_first_time_login(self,obj):
        qs = Profile.objects.get(owner__username = obj['username'])
        if qs.name is None:
            return True
        return False

    class Meta:
        model = User
        fields = ['id','username','email','password','tokens','first_time_login']

    def validate(self,attrs):
        username =  attrs.get('username','')
        password =  attrs.get('password','')
        user_obj_email = User.objects.filter(email=username).first()
        user_obj_username = User.objects.filter(username=username).first()
        if user_obj_email:
            user = auth.authenticate(username = user_obj_email.username,password=password)
            if user_obj_email.auth_provider != 'email':
                raise AuthenticationException(
                    'Please continue your login using ' + user_obj_email.auth_provider)
            if not user:
                raise AuthenticationException('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationException('Account disabled. contact admin')
            if not user.is_verified:
                email = user.email
                token = RefreshToken.for_user(user).access_token
                current_site = self.context.get('current_site')
                relative_link = reverse('email-verify')
                absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
                email_body = {}
                email_body['username'] = user.username
                email_body['message'] = 'Use link below to verify your email'
                email_body['link'] = absurl
                data = {'email_body' : email_body,'email_subject' : 'Verify your email','to_email' : user.email}
                Util.send_email(data)
                raise AuthenticationException('Email is not verified, A Verification Email has been sent to your email address')
            return {
                'email' : user.email,
                'username' : user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        if user_obj_username:
            user = auth.authenticate(username = username,password=password)
            if not user:
                raise AuthenticationException('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationException('Account disabled. contact admin')
            if not user.is_verified:
                email = user.email
                token = RefreshToken.for_user(user).access_token
                current_site = self.context.get('current_site')
                relative_link = reverse('email-verify')
                absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
                email_body = {}
                email_body['username'] = user.username
                email_body['message'] = 'Use link below to verify your email'
                email_body['link'] = absurl
                data = {'email_body' : email_body,'email_subject' : 'Verify your email','to_email' : user.email}
                Util.send_email(data)
                raise AuthenticationException('Email is not verified, A Verification Email has been sent to your email address')
            return {
                'email' : user.email,
                'username' : user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        raise AuthenticationException('Invalid credentials. Try again')
    
class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255,required=True)

    class Meta:
        fields = ['email']

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    age = serializers.IntegerField(required=True)
    aadhar = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    status = serializers.CharField(read_only=True)
    latitude = serializers.DecimalField(max_digits=15, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=15, decimal_places=6)
    received = serializers.IntegerField(required=True)
    special = serializers.BooleanField(required=True)
    
    def validate_aadhar(self,attrs):
        curr_user = self.context.get('user')
        if len(attrs) != 12:
            raise ValidationException("The length of Aadhar Card should be exactly 12 characters")
        if Aadhar.objects.filter(aadhar=attrs).exists():
            check = Aadhar.objects.get(aadhar=attrs)
            if check.user.username != curr_user:
                raise ValidationException("Your Aadhar Card needs to be unique")
        user = User.objects.get(username=curr_user)
        here = Aadhar.objects.filter(user=user)
        if here.exists():
            another = Aadhar.objects.get(user=user)
            another.aadhar = attrs
            another.save()
        else:
            Aadhar.objects.create(user=user,aadhar=attrs)
        return attrs
    
    def validate_phone(self,attrs):
        if len(attrs) != 10:
            raise ValidationException("The Phone Number should be exactly 10 digits")
        return attrs
            
    def validate_received(self,attrs):
        if int(attrs) < 0 or int(attrs) > 2:
            raise ValidationException("Received Doses can only be between 0 and 2")
        return attrs
    class Meta:
        model = Profile
        fields = ['name','age','aadhar','phone','status','latitude','longitude','received','special']
        
class RequestPasswordResetEmailSeriliazer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationException('The reset link is invalid')

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationException('The reset link is invalid')
        return super().validate(attrs)

class PasswordChangeSerializer(serializers.Serializer):
    old_pass = serializers.CharField(max_length = 68,min_length = 6,required=True)
    new_pass = serializers.CharField(max_length = 68,min_length = 6,required=True)

    class Meta:
        fields = ['old_pass','new_pass']
