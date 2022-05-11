from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import auth_user, create_token, get_user_from_token, create_user, read_user_info, update_user
from config import get_settings

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

settings = get_settings()

@app.post('/login', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form.username, form.password)
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer"
    }

@app.post('/signup', response_model=UserRes)
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form('')
):
    new_user = create_user(username, password, email)
    return new_user

@app.get('/user/me', response_model=UserRes)
async def get_me(cur_user: UserRes = Depends(get_user_from_token)):
    return cur_user

@app.get('/user/', response_model=UserRes)
async def get_other(
    username: str = '',
    cur_user: UserRes = Depends(get_user_from_token)
):
    return read_user_info(username)

@app.post('/update_user', response_model=UserRes)
async def change_info(
    old_pass: str = Form(...),
    new_pass: str = Form(...),
    new_email: str = Form(...),
    cur_user: UserRes = Depends(get_user_from_token)
):
    check_user = auth_user(cur_user.username, old_pass)
    if check_user.id != cur_user.id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return update_user(check_user.username, new_pass, new_email)