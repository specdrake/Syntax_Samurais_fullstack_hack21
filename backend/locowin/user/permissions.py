from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS

class AuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user or request.user.is_authenticated or request.method in SAFE_METHODS:
            return True
        else:
            raise Forbidden
    
class ForbiddenAdmin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'status' : "FAILED",
        'error':'Only Admins can access this page'
    }

class AuthenticatedAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        else:
            raise ForbiddenAdmin

class ForbiddenOfficer(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'status' : "FAILED",
        'error':'Only Vaccination officers can access this page'
    }

class AuthenticatedOfficer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.officer:
            return True
        else:
            raise ForbiddenAdmin

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class Forbidden(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'status' : "FAILED",
        'error':'Authentication credentials were not provided'
    }

class Authenticated(permissions.BasePermission):

    def has_permission(self,request,view):
        if not request.user or not request.user.is_authenticated:
            raise Forbidden
        else :
            return True
