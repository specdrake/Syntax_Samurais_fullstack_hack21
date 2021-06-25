from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import User,Profile,Aadhar
from .exception import *
import re


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
