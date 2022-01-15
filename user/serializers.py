from rest_framework import serializers
from user.models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'password',
                  'role')
