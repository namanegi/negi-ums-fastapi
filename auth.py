from fastapi import Depends, HTTPException
import hashlib
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt

from DBMgr import User, Session
from config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = get_settings()
secret_key = settings.jwt_secret_key

def auth_user(username: str, password: str):
    user = User.get(username=username)
    if not user:
        raise HTTPException(status_code=404, detail='user not exists')
    if hashlib.sha256(password.encode()).hexdigest() != user.password:
        raise HTTPException(status_code=401, detail='password ERROR')
        # return 'password error'
    return user

def read_user_info(username: str):
    try:
        return User.get(username=username)
    except:
        raise HTTPException(status_code=404, detail='User not exists')

def create_token(user_id: int):
    token_payload = {
        "user_id": user_id,
        "expired_at": (datetime.utcnow() + timedelta(days=3)).timestamp()
    }
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    Session.update(token=token).where(Session.tid == user_id).execute()
    return token

def create_user(username: str, password: str, email: str = ''):
    user = None
    try:
        user = User.get(username=username)
    except:
        pass
    if user:
        raise HTTPException(status_code=409, detail='User existed')
    tmp = User.create(
        username=username,
        password=hashlib.sha256(password.encode()).hexdigest(),
        email=email
    )
    token_payload = {
        "user_id": tmp.id,
        "expired_at": (datetime.utcnow() + timedelta(days=3)).timestamp()
    }
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    Session.create(tid=tmp.id, token=token)
    return tmp

def update_user(username: str, password: str, email: str):
    User.update(
        password=hashlib.sha256(password.encode()).hexdigest(),
        email=email
    ).where(User.username == username).execute()
    return User.get(username=username)

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
