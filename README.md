# negi-ums-fastapi

## Introducton
* A new version of negi-ums, with modern lib like fastapi, pydantic, peewee, etc.

## Launch Step
```
pip install -r requirements.txt
echo JWT_SECRET_KEY="XXXXXXXX" >> .env
uvicorn negi-ums:app --reload
```