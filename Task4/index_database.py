import peewee 


db = peewee.SqliteDatabase('index_file.db')

def ensure_creation():
    was_closed = db.is_closed()
    if was_closed:
        db.connect()
    db.create_tables([Words, Urls, References, WordsReferences])

    if was_closed:
        db.close()

class BaseModel(peewee.Model):
    class Meta:
        database = db


class Words(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    term = peewee.CharField(unique=True)


class Urls(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    url = peewee.CharField(unique=True)
    is_indexed = peewee.BooleanField(default=False)

class References(BaseModel):
    reference_from = peewee.ForeignKeyField(Urls, backref='reference_from')
    reference_to = peewee.ForeignKeyField(Urls, backref='reference_to')

class WordsReferences(BaseModel):
    referenced_word = peewee.ForeignKeyField(Words, backref='referenced_word')
    page_url = peewee.ForeignKeyField(Urls, backref='page_url')

    class Meta:
        constraints = [peewee.SQL('UNIQUE (referenced_word_id, page_url_id)')]



def connect():
    db.connect(True)
    ensure_creation()

def close():
    db.close()
