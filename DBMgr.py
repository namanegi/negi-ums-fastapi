from peewee import SqliteDatabase, Model, AutoField, CharField, TextField, ForeignKeyField

db = SqliteDatabase('./db/db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField(100, unique=True)
    password = TextField()
    email = CharField(null=False)

class Session(BaseModel):
    tid = ForeignKeyField(User, backref='user_id')
    token = TextField()

def init_db():
    db.create_tables([User])
    db.create_tables([Session])

if __name__ == '__main__':
    init_db()