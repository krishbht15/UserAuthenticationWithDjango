import base64
import re


def encodePassword(pwdString):
    return base64.b64encode(pwdString.encode("utf-8"))


def decodePwd(encodedPwd):
    return base64.b64decode(encodedPwd).decode("utf-8")


def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


def validateUser(email, username, password):
    if validateEmail(email) == False:
        raise Exception("Validation failed: Email is invalid.")
    if len(username) < 5: raise Exception("Validation failed: Username is invalid.")
    if len(password) < 5: raise Exception("Validation failed: Password is invalid.")
