# Create your views here.
from datetime import datetime

from django.core import exceptions
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from user.models import User
from user_auth import security
from user_auth.roles import Roles
from . import util
from .serializers import UserResponseSerializer


# TODO

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user(request):
    user = security.authenticate_token(request)
    if (user is None) | (user.count() == 0):
        raise exceptions.ObjectDoesNotExist("Authentication error")
    if request.method == "GET":
        return JsonResponse(UserResponseSerializer(user.first()).data, safe=False)
    elif request.method == "POST":
        if user.first().role != Roles.SUPER_ADMIN:
            raise exceptions.BadRequest("User not allowed")
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        util.validateUser(email, username, password)
        encryptedPassword = util.encodePassword(password)
        if User.objects.filter(Q(username=username) | Q(email=email)).first() is not None:
            raise Exception("Username or Email already exists")
        user = User(username=username, email=email, password=encryptedPassword, role=role)
        user.jwt = security.generate_access_token(user)
        user.save()
        return JsonResponse({"response": user.jwt})
    elif request.method == "DELETE":
        if user.first().role != Roles.SUPER_ADMIN:
            raise exceptions.BadRequest("User not allowed")
        isUpdated = user.update(deleted_at=datetime.utcnow())
        if isUpdated == 1: return JsonResponse({"message": "Deleted Successfully"})
        return JsonResponse({"message": "Something went wrong"})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        encryptedPassword = util.encodePassword(password)
        user = User.objects.filter(Q(email=email) & Q(password=encryptedPassword) & Q(deleted_at=None))
        if user.first() is None:
            raise exceptions.ObjectDoesNotExist("User doesn't exist")
        jwt = security.generate_access_token(user.first())
        user.update(jwt=jwt)
        return JsonResponse({"token": jwt})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")


@api_view(['GET'])
def logout(request):
    if request.method == "GET":
        user = security.authenticate_token(request)
        if (user is None) | (user.count() == 0):
            raise exceptions.ObjectDoesNotExist("User doesn't exist")
        isUpdated = user.update(jwt=None)
        if isUpdated == 1: return JsonResponse({"message": "Logged Out Successfully"})
        return JsonResponse({"message": "Something went wrong"})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def accessResources(request):
    user = security.authenticate_token(request)
    if (user is None) | (user.count() == 0):
        raise exceptions.ObjectDoesNotExist("User doesn't exist")
    method = request.method
    if method == "GET":
        return JsonResponse({"message": "Read Successfully"})
    elif method == "POST":
        if user.first().role != Roles.SUPER_ADMIN:
            raise exceptions.BadRequest("User not allowed to create.")
        return JsonResponse({"message": "Created Successfully"})
    elif method == "PUT":
        if user.first().role == Roles.READ_ONLY: raise exceptions.BadRequest("User not allowed to create.")
        return JsonResponse({"message": "Updated Successfully"})
    elif method == "DELETE":
        if user.first().role != Roles.SUPER_ADMIN: raise exceptions.BadRequest("User not allowed to create.")
        return JsonResponse({"message": "Delete Successfully"})
    return None
