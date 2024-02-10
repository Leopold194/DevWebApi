import jwt
import datetime
import exceptions.exceptions as exce

def encode_auth_token(user_id, secret_key, duration = 3600):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=duration),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token, secret_key):
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise exce.ExpiredToken()
    except jwt.InvalidTokenError:
        raise exce.InvalidToken()