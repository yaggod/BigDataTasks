import peewee 
from typing import Iterator


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

    def get_all_indexed_pages() -> Iterator['Urls']:
        return Urls.select().where(Urls.is_indexed == True)
    
    def get_all_pages() -> Iterator['Urls']:
        return Urls.select()

    def get_all_outgoing_links(self) -> Iterator['Urls']:
        return map(lambda item : item.reference_to, References
                   .select()
                   .where(References.reference_from == self))
    
    def get_all_indexed_outgoing_links(self) -> Iterator['Urls']:
        return filter(lambda item : item.is_indexed , map(lambda item : item.reference_to, References
                   .select()
                   .where(References.reference_from == self)))
    
    def get_all_incoming_links(self) -> Iterator['Urls']:
                return map(lambda item : item.reference_to, References
                   .select()
                   .where(References.reference_to == self)) 

    def get_all_indexed_incoming_links(self) -> Iterator['Urls']:
                return filter(lambda item : item.is_indexed, map(lambda item : item.reference_to, References
                   .select()
                   .where(References.reference_to == self)))

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
