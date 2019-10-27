import sys
try:
    import jwt
except Exception as e:
    print(str(e) + ". Please install it")
    sys.exit(1)

class Authorizer:
    def __init__(self):
        pass

    def read_secret(self):
        f = open("../../authority/key", "r")
        key = f.readline()
        f.close()
        return key.rstrip()

    def create_token(self):
        #secret = self.read_secret()
        secret = "This is a random key please change me"
        encoded_jwt = jwt.encode({}, secret, algorithm='HS256')
        return encoded_jwt

    def verify_token(self, encoded_jwt):
        #secret = self.read_secret()
        secret = "This is a random key please change me"
        try:
            jwt.decode(encoded_jwt, secret, algorithms=['HS256'])
            return True
        except Exception as e:
            return False
