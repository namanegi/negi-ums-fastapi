from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from DBMgr import clear_all_db
from auth import auth_user, create_token, get_user_from_token, create_user, read_user_info, update_user
from config import get_settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInfoForm(OAuth2PasswordRequestForm):
    email: str = ''

class UpdateUserInfoForm(UserInfoForm):
    new_password: str
    new_email: str = ''

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

@app.post(
    '/login',
    response_model=Token,
    description="The API for login, returns Bearer token"
)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form.username, form.password)
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer"
    }

@app.post(
    '/signup',
    response_model=UserRes,
    description="regist a new account in ums, unique username requested"
)
async def sign_up(form: UserInfoForm = Depends()):
    new_user = create_user(form.username, form.password, form.email)
    return new_user

@app.get(
    '/user/me',
    response_model=UserRes,
    description="The API for validating token and get self info"
)
async def get_self_and_auth(cur_user: UserRes = Depends(get_user_from_token)):
    return cur_user

@app.get('/user/', response_model=UserRes)
async def get_other(
    username: str = '',
    cur_user: UserRes = Depends(get_user_from_token)
):
    return read_user_info(username)

@app.post('/update_user', response_model=UserRes)
async def change_info(
    form: UpdateUserInfoForm = Depends(),
    cur_user: UserRes = Depends(get_user_from_token)
):
    check_user = auth_user(cur_user.username, form.password)
    if check_user.id != cur_user.id:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return update_user(check_user.username, form.new_password, form.new_email)

@app.get('/secret')
async def test():
    return settings.jwt_secret_key

@app.get('/delete_all')
async def runle():
    clear_all_db()
    return {}