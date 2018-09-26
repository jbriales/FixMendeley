#!/usr/bin/env python3
# coding=utf-8
"""
Explore and fix different Mendeley database issues
"""

import argparse
import sys
from termcolor import colored

from fixmendeley.my_mendeley_models import *
# from .scripts.pwizmodels2mymodels import fields_of_interest

# DEBUG: Print all queries to stderr.
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(
    description=__doc__,
    epilog="By Jesus Briales"
)
subparsers = parser.add_subparsers()

from fixmendeley.fuse_entries import find_duplicates_and_fuse, fuse_fields
find_duplicates_and_fuse.parser = subparsers.add_parser(
    'fuse-entries',
    description=find_duplicates_and_fuse.__doc__)
find_duplicates_and_fuse.parser.set_defaults(func=find_duplicates_and_fuse)
find_duplicates_and_fuse.parser.add_argument('field')
find_duplicates_and_fuse.parser.add_argument('value')
find_duplicates_and_fuse.parser.add_argument('--do_delete_remaining', action='store_true')


from fixmendeley.fix_venues import fix_venues
fix_venues.parser = subparsers.add_parser(
    'fix-venues',
    description=fix_venues.__doc__)
fix_venues.parser.set_defaults(func=fix_venues)


from fixmendeley.fix_via_dblp import fix_via_dblp
fix_via_dblp.parser = subparsers.add_parser(
    'fix_via_dblp',
    description=fix_venues.__doc__)
fix_via_dblp.parser.set_defaults(func=fix_via_dblp)


def test():
    # Organize docs into a dictionary by citation key to find conflicts
    docs_by_key = dict()

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


test.parser = subparsers.add_parser(
    'test',
    description=test.__doc__)
test.parser.set_defaults(func=test)


def main():
    if len(sys.argv) <= 1:
        parser.print_help()
        return True

    # NOTE: Can this be simplified? Check doc
    kwargs = dict(parser.parse_args(sys.argv[1:])._get_kwargs())
    func = kwargs.pop('func')

    successful = func(**kwargs)
    sys.exit(0 if successful else 1)


if __name__ == '__main__':
    main()
