from fastapi import Depends, HTTPException
import hashlib
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from functools import lru_cache

from DBMgr import User, Session
import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache()
def get_settings():
    print()
    return config.Settings()

settings = get_settings()
secret_key = settings.jwt_secret_key

def auth_user(username: str, password: str):
    user = User.get(username=username)
    if hashlib.sha256(password.encode()).hexdigest() != user.password:
        raise HTTPException(status_code=401, detail='password ERROR')
        # return 'password error'
    return user

def create_token(user_id: int):
    token_payload = {
        "user_id": user_id,
        "expired_at": (datetime.utcnow() + timedelta(days=3)).timestamp()
    }
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    Session.update(token=token).where(Session.tid == user_id).execute()
    return token

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        session = Session.get(token=token)
    except:
        raise HTTPException(status_code=401, detail='Token not found')
    payload = jwt.decode(session.token, secret_key, algorithms='HS256')
    if "user_id" not in payload or "expired_at" not in payload:
        raise HTTPException(status_code=401, detail='Permission denied')
    if payload["expired_at"] < datetime.now().timestamp():
        raise HTTPException(status_code=402, detail='Expired')
    return User.get(id=payload["user_id"])

if __name__ == '__main__':
    for item in Session.select():
        print(item.tid, item.token)
    token = create_token(1)
    print(token['token'])
    for item in Session.select():
        print(item.tid, item.token)
    print(get_user_from_token(token["token"]).username)
    print(get_user_from_token(1))
