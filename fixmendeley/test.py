#!/usr/bin/env python3
# coding=utf-8
"""
Play with some peewee stuff
"""

from termcolor import colored

from fixmendeley.my_mendeley_models import *
from fixmendeley.fuse_entries import find_duplicates_and_fuse, fuse_fields


def test():
    # Find repeated titles
    query_repeated_rows = (
        Document
        .select(Document.title, fn.COUNT(Document.id).alias('num_entries'))
        .group_by(Document.title)
        .having(SQL('num_entries') > 1)
    )
    repeated_titles = list()
    for entry in query_repeated_rows:
        print("%s x %s" % (entry.title, entry.num_entries))
        repeated_titles.append(entry.title)
    print(colored("There are %s repeated titles" % len(repeated_titles), 'red'))

    # Test peewee-agnostic function
    find_duplicates_and_fuse('title', repeated_titles[0], do_delete_remaining=False)

    # Fuse fields of rows with repeated title into a single row
    for title in repeated_titles:
        query = Document.select().prefetch(Author, Url, Tag).where(Document.title == title)
        print("Fixing %s" % title)
        print("===================")
        fuse_fields(query, do_delete_remaining=False)

    return True

    # Find repeated citation keys
    # SQL statement: `SELECT DataId, COUNT(*) c FROM DataTab GROUP BY DataId HAVING c > 1;`
    query_repeated_rows = (
        Document
        .select(Document.citationkey, fn.COUNT(Document.id).alias('num_entries'))
        .group_by(Document.citationkey)
        .having(SQL('num_entries') > 1)
    )
    repeated_citationkeys = list()
    for entry in query_repeated_rows:
        print("%s x %s" % (entry.citationkey, entry.num_entries))
        repeated_citationkeys.append(entry.citationkey)
    print(colored("There are %s repeated citation keys" % len(repeated_citationkeys), 'red'))

    for citationkey in repeated_citationkeys:
        query = Document.select().prefetch(Author, Url, Tag).where(Document.citationkey == citationkey)
        print("Fixing %s" % citationkey)
        print("===================")
        fuse_fields(query, do_delete_remaining=False)

    return True
