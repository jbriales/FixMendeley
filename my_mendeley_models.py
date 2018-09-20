from peewee import *

database = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})


class BaseModel(Model):
    class Meta:
        database = database

# List of Mendeley fields of interest
class Document(BaseModel):
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



@inproceedings{dube2016non,
author = {Dub{\'{e}}, Renaud and Sommer, Hannes and Gawel, Abel and Bosse, Michael and Siegwart, Roland},
booktitle = {Robot. Autom. (ICRA), 2016 IEEE Int. Conf.},
file = {:home/jesus/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/Dub{\'{e}} et al. - 2016 - Non-uniform sampling strategies for continuous correction based trajectory estimation.pdf:pdf},
organization = {IEEE},
pages = {4792--4798},
title = {{Non-uniform sampling strategies for continuous correction based trajectory estimation}},
year = {2016}
}