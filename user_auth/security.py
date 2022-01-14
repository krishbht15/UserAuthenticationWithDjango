import datetime

import jwt
from django.db.models import Q
from jwt import exceptions


from user.models import User
from . import settings


def generate_access_token(user):
    access_token_payload = {
        'user_id': str(user.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'role': user.role
    }
    print(access_token_payload)
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    print("bjksbakj" + access_token)
    return access_token


def authenticate_token(request):
    try:
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        access_token = authorization_header.split(' ')[1]
        print(access_token)
        if not authorization_header:
            return None
        print(access_token)
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user = User.objects.filter(Q(jwt=access_token) & Q(deleted_at=None))
        print(user)
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        return user
    except IndexError:
        raise exceptions.AuthenticationFailed('Token prefix missing')
    except jwt.exceptions.ExpiredSignatureError:
        print("Invalid Token")
        User.objects.filter(jwt=access_token).update(jwt=None)
        return None
    except Exception:
        raise exceptions.InvalidTokenError("Authorization is not present")