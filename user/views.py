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
    if user is None:
        raise exceptions.ObjectDoesNotExist("User doesn't exist")
    if request.method == "GET":
        print("dkjanbsjknsjk")
        return JsonResponse(UserResponseSerializer(user.first()).data, safe=False)
    elif request.method == "POST":
        if user.first().role != Roles.SUPER_ADMIN:
            raise exceptions.BadRequest("User not allowed")
        print(request.data.get('username'))
        username = request.data.get('username')
        email = request.data.get('email')
        password = util.encodePassword(request.data.get('password'))
        role = request.data.get('role')
        user = User(username=username, email=email, password=password, role=role)
        # print(serial.data.get('username'))
        print("dsakdsj  " + username)
        print(user.id)
        user.jwt = security.generate_access_token(user)
        user.save()
        return JsonResponse({"response": user.jwt})
    # elif request.method == "PUT":
    #     print("dsda")
    elif request.method == "DELETE":
        if user.first().role != Roles.SUPER_ADMIN:
            raise exceptions.BadRequest("User not allowed")
        isUpdated = user.update(deleted_at=datetime.utcnow())
        if isUpdated == 1: return JsonResponse({"message": "Deleted Successfully"})
        return JsonResponse({"message": "Something went wrong"})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")


@api_view(['POST'])
def login(request):
    print("starting")
    if request.method == "POST":
        print("post")
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)
        encryptedPassword = util.encodePassword(password)
        print(encryptedPassword)
        user = User.objects.filter(Q(email=email) & Q(password=encryptedPassword) & Q(deleted_at=None))
        if user.first() is None:
            raise exceptions.ObjectDoesNotExist("User doesn't exist")
        print(user.first().deleted_at)
        jwt = security.generate_access_token(user.first())
        user.update(jwt=jwt)
        return JsonResponse({"token": jwt})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")


@api_view(['GET'])
def logout(request):
    if request.method == "GET":
        user = security.authenticate_token(request)
        if user is None:
            raise exceptions.ObjectDoesNotExist("User doesn't exist")
        isUpdated = user.update(jwt=None)
        print(isUpdated)
        if isUpdated == 1: return JsonResponse({"message": "Logged Out Successfully"})
        return JsonResponse({"message": "Something went wrong"})
    raise exceptions.PermissionDenied("Resource Doesn't Exist")
