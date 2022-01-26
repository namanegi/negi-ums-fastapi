from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import auth_user, create_token, get_user_from_token
from functools import lru_cache

import config

app = FastAPI()

class UserRes(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

@lru_cache()
def get_settings():
    print()
    return config.Settings()

settings = get_settings()

@app.post('/token', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form.username, form.password)
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer"
    }

@app.post('/signup')
async def signup(form: OAuth2PasswordRequestForm = Depends()):
    return {
        "user": form.username
    }

@app.get('/users/me', response_model=UserRes)
async def get_me(cur_user: UserRes = Depends(get_user_from_token)):
    return cur_user