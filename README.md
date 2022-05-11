# negi-ums-fastapi

## Introducton
* A new version of negi-ums, with modern lib like fastapi, pydantic, peewee, etc.
### API
* /signup API for registing new user
  * users should have unique username
* /login for login, receiving bearer token
* /user/me for getting self info
* /users for getting info of other user
* /update_user for update self info such as pw and email

## Launch Step
```
pip install -r requirements.txt
echo JWT_SECRET_KEY="XXXXXXXX" >> .env
uvicorn negi-ums:app --reload
```
## Swagger
* Auto Swagger page by FastAPI
  * hosturl/docs
    * http://localhost:8000/docs#/