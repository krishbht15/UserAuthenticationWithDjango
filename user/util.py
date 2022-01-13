import base64


def encodePassword(pwdString):
    return base64.b64encode(pwdString.encode("utf-8"))


def decodePwd(encodedPwd):
    return base64.b64decode(encodedPwd).decode("utf-8")
