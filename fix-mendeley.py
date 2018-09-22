#!/usr/bin/env python3
# coding=utf-8
"""
Explore and fix different Mendeley database issues
"""

from termcolor import colored

from my_mendeley_models import *

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})
# DEBUG: Print all queries to stderr.
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


def main():
    # Organize docs into a dictionary by citation key to find conflicts
    docs_by_key = dict()

    # Find repeated keys
    query = Document.select().prefetch(Author, Url, Tag).order_by(Document.citationkey)
    with db.atomic():
        for doc in query:
            docs_by_key.setdefault(doc.citationkey, []).append(doc.__data__)

    # Check documents without key (and remove if another better document exists)
    docs_without_key = docs_by_key.pop(None)
    print("Docs without key")
    if False:
        for entry in docs_without_key:
            print("- {}".format(entry['title']))
            query = Document.select().prefetch(Author, Url, Tag).where(Document.title.contains(entry['title']))
            with db.atomic():
                for doc in query:
                    print("- {}".format(doc.title))

    print("Docs with conflicting key")
    for key, entries in docs_by_key.items():
        print("Citation key: " + key)
        for entry in entries:
            print("{id}:\t{citationkey} -> {title}".format(**entry))

    return True


if __name__ == '__main__':
    main()
