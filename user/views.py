# Create your views here.
from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view

from user.models import User
from . import util
from .serializers import UserSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user(request):
    if request.method == "GET":
        a = UserSerializer(User.objects.all()[3]).data
        print(a)
        return JsonResponse(a)
    elif request.method == "POST":
        print(request.data.get('username'))
        serial = UserSerializer(request.data)
        username = serial.data.get('username')
        email = serial.data.get('email')
        password = util.encodePassword(serial.data.get('password'))
        role = serial.data.get('role')
        user = User(username=username, email=email, password=password, role=role,
                    created_at=datetime.today(),
                    updated_at=datetime.today(), deleted_at=datetime.today())
        print(serial.data.get('username'))
        print("dsakdsj  " + username)
        user.save()
        return JsonResponse({"response": "created successfully"})
    elif request.method == "PUT":
        print("dsda")
    elif request.method == "DELETE":
        print("kknsdkjan")
    return None
