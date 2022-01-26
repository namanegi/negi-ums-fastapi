import hashlib

from DBMgr import Session, User, init_db
from auth import auth_user
from datetime import datetime, timedelta
from jose import jwt

def insertTest():
    user_case = [
        {
            "username": "Amy",
            "password": "secret_amy",
            "email": ""
        },
        {
            "username": "Bob",
            "password": "secret_bob",
            "email": "bob@test.com"
        }
    ]
    init_db()
    for user in user_case:
        new_user = User.create(username=user["username"], password=hashlib.sha256(user["password"].encode()).hexdigest(), email=user["email"])
        token_payload = {
        "user_id": new_user.id,
        "expired_at": (datetime.utcnow() + timedelta(days=3)).timestamp()
        }
        token = jwt.encode(token_payload, 'TEST1234567', algorithm='HS256')
        Session.create(tid=new_user.id, token=token)

if __name__ == '__main__':
    insertTest()
    # print(auth_user('Amy', 'secret_amy'))