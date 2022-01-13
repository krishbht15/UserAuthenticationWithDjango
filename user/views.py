# Create your views here.
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializerss import UserSerializer
from user.models import User


@api_view(['GET', 'POST'])
def signup(request):
    print(request.data.get('username'))
    if request.method == "POST":
        serial = UserSerializer(request.data)
        username = serial.data.get('username')
        email = serial.data.get('email')
        password = serial.data.get('password')
        role = serial.data.get('role')
        user = User(username=username, email=email, password=password, role=role,
                    created_at=datetime.today(),
                    updated_at=datetime.today(), deleted_at=datetime.today())
        print(serial.data.get('username'))
        print("dsakdsj  " + username)
        user.save()
    return Response("created successfully")
