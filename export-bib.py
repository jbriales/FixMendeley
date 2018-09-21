#!/usr/bin/env python3
# coding=utf-8
"""
Documentation
"""

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from termcolor import colored
import json
import os
import subprocess

from my_mendeley_models import *
# from mendeley_models import *

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})

mend_to_bib_types = json.load(open('mend2bib.json', 'r'))


def main():
    # Initialize bibtex database
    bibdb = BibDatabase()
    # bibdb.entries = [
    #     {'ENTRYTYPE': 'article',
    #      'ID': 'Cesar2013',
    #      'journal': 'Nice Journal',
    #      'comments': 'A comment',
    #      'pages': '12--23',
    #      'month': 'jan',
    #      'abstract': 'This is an abstract. This line should be long enough to test\nmultilines...',
    #      'title': 'An amazing title',
    #      'year': '2013',
    #      'volume': '12',
    #
    #      'author': 'Jean César',
    #      'keyword': 'keyword1, keyword2'
    #     }]

    # Populate bibtex database from Mendeley database via peewee
    for doc in Document.select():
        # print(doc.title)
        entry = {
            'ENTRYTYPE': mend_to_bib_types[doc.type],
            'ID': doc.citationkey,
            'title': doc.title
        }
        if not entry['ID']:
            print(colored("Missing key for %s" % doc.title, 'red'))
            continue
        bibdb.entries.append(entry)

    # Write bibtex database to file
    writer = BibTexWriter()
    writer.indent = '  '  # indent entries with 4 spaces instead of one
    # writer.comma_first = True  # place the comma at the beginning of the line
    with open('bibtex.bib', 'w') as bibfile:
        bibfile.write(writer.write(bibdb))

    return True


if __name__ == '__main__':
    main()
