from peewee import *

database = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})


class BaseModel(Model):
    class Meta:
        database = database


# List of Mendeley fields of interest
class Document(BaseModel):
    # id = IntegerField(db_column='id', primary_key=True, null=False, index=True)
    abstract = CharField(null=True)
    added = IntegerField(null=True)
    arxivid = CharField(db_column='arxivId', null=True)
    citationkey = CharField(db_column='citationKey', null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    dateaccessed = CharField(db_column='dateAccessed', null=True)
    doi = CharField(null=True)
    importer = CharField(null=True)
    institution = CharField(null=True)
    modified = IntegerField(null=True)
    month = IntegerField(null=True)
    pages = CharField(null=True)
    publication = CharField(null=True)
    sourcetype = CharField(db_column='sourceType', null=True)
    title = CharField(null=True)
    type = CharField(null=True)
    volume = CharField(null=True)
    year = IntegerField(null=True)

    class Meta:
        db_table = 'Documents'


class Author(BaseModel):
    # documentid = IntegerField(db_column='documentId', index=True)
    documentid = ForeignKeyField(db_column='documentId', field='id', model=Document, unique=True, backref='authors')
    firstnames = CharField(db_column='firstNames', null=True)
    lastname = CharField(db_column='lastName')

    class Meta:
        db_table = 'DocumentContributors'


class Url(BaseModel):
    # documentid = IntegerField(column_name='documentId')
    documentid = ForeignKeyField(db_column='documentId', field='id', model=Document, backref='urls')
    position = IntegerField()
    url = CharField()

    class Meta:
        table_name = 'DocumentUrls'
        indexes = (
            (('documentid', 'position'), True),
        )
        primary_key = CompositeKey('documentid', 'position')


class Tag(BaseModel):
    documentid = ForeignKeyField(db_column='documentId', field='id', model=Document, backref='urls')
    tag = CharField()

    class Meta:
        table_name = 'DocumentTags'
        indexes = (
            (('documentid', 'tag'), True),
        )
        primary_key = CompositeKey('documentid', 'tag')
