#!/usr/bin/env python3
# coding=utf-8
"""
Explore and fix different Mendeley database issues
"""

from termcolor import colored

from peewee import SqliteDatabase
from fixmendeley.my_mendeley_models import *
# from .scripts.pwizmodels2mymodels import fields_of_interest

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})
# DEBUG: Print all queries to stderr.
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# @db.aggregate('myfun')
# class myfun(object):
#     def __init__(self):
#         self.entries = []
#
#     def step(self, doc):
#         self.entries.append(doc)
#
#     def finalize(self):
#         return self.entries


fields_of_interest = [
    'abstract',
    'added',
    # 'modified', # not important
    # 'importer', # give manually
    'arxivid',
    'citationkey',
    'city',
    'country',
    # 'dateaccessed', # not important
    'doi',
    'institution',
    'isbn',
    'issn',
    'issue',
    'month',
    'pages',
    'publication',
    'publisher',
    'sourcetype',
    'title',
    'type',
    'volume',
    'year',
]

conflict_solver = dict()
conflict_solver['added'] = min

# Delete repeated entries once fused in once
do_delete = False


def find_duplicates_and_fuse(field, value, do_delete_remaining=False):
    query = Document.select().prefetch(Author, Url, Tag).where(getattr(Document, field) == value)
    fuse_fields(query, do_delete_remaining=do_delete_remaining)


def fuse_fields(query, do_delete_remaining=False):
    """
    Fuse fields from several potentially equivalent documents into first one
    :param query: SQL query with conflicting/repeated rows
    :param do_delete_remaining: delete repeated rows after collecting all fields in one
    """

    # TEMP FIX for import?
    # from .my_mendeley_models import Document, Author, Url, Tag, File, DocumentFile
    # from my_mendeley_models import Document, Author, Url, Tag, File, DocumentFile

    with db.atomic():
        # Create new doc that gathers all available information (if not conflicting)
        # base_doc = Document()
        # base_doc.citationkey = citation_key
        # Use first doc in the query as base (to keep non-trivial fields already populated)
        # base_doc = query.first()
        base_doc = query[0]
        base_doc.importer = 'PythonImporter'

        # About authors
        # Document-Author relation is one-to-many
        # Each row in DocumentContributors has fields 'documentid', 'contribution', 'firsnames' and 'lastname'
        # TODO: Author list should be fine for every document, but fix right names
        # Sanity check: every row has the same number of authors
        set_nums = set()
        for doc in query:
            set_nums.add(len(doc.authors))
        assert len(set_nums) == 1, "Conflicting lists of authors"

        # Gather all URLs
        set_urls = set()
        for doc in query:
            print("id %s" % doc.id)
            for url in doc.urls:
                print("- {}: {}".format(url.position, url.url))
                set_urls.add(url.url)
                # TODO: Delete this (will be created again later)
        # Create new URLs linked to base document
        # Document-URL relation is one-to-many
        # Each row in DocumentUrls has fields 'documentid', 'position' and 'url'
        # We can rewrite URLs in whichever order (or not? depends on how we can to export URLs later)
        print(colored("Creating DocumentUrls entries for doc <%s>" % base_doc.id, 'yellow'))
        for idx, url in enumerate(set_urls):
            print('%s %s' % (idx, url))
            new_url = Url(documentid=base_doc.id, position=idx, url=url)
            try:
                num_new_rows = new_url.save(force_insert=True)
                assert num_new_rows > 0, colored("ERROR: No row was created", 'red')
            except IntegrityError:
                print(colored('ERROR: Entry already exists', 'red'))

        # Gather all tags
        set_tags = set()
        for doc in query:
            for tag in doc.tags:
                set_tags.add(tag.tag)
                # TODO: Delete this (will be created again later)
        # Create new tags linked to base document
        # Document-tag relation is one-to-many
        # Each row in DocumentUrls has fields 'documentid' and 'tag'
        print(colored("Creating DocumentTags entries for doc <%s>" % base_doc.id, 'yellow'))
        for tag in set_tags:
            new_tag = Tag(documentid=base_doc.id, tag=tag)
            try:
                num_new_rows = new_tag.save(force_insert=True)
                assert num_new_rows > 0, colored("ERROR: No row was created", 'red')
            except IntegrityError:
                print(colored('ERROR: Entry already exists', 'red'))

        # Fix attached files (some entries miss the PDF doc)
        # Table 'Files' contains 'hash' and 'localUrl' for every existing PDF file
        # Table 'DocumentFiles' contains many-to-many correspondences between doc and files
        # with each row having fields 'documentId', 'hash', 'remoteFileUuid'
        # To attach PDF to doc, create row in DocumentFiles (many-to-many table)
        # Gather all files for a certain doc
        set_values = set()
        for doc in query:
            for pdf in doc.files:
                print('id %s, hash %s, remote_uuid %s' % (pdf.documentid, pdf.hash, pdf.remotefileuuid))
                set_values.add((pdf.hash, pdf.remotefileuuid))
                # TODO: Delete this (will be created again later)
        # Create new DocumentFile entries to attach PDFs to docs
        # Document-tag relation is one-to-many
        # Each row in DocumentUrls has fields 'documentid' and 'tag'
        print(colored("Creating DocumentFiles entries for doc <%s>" % base_doc.id, 'yellow'))
        for (hash, remotefileuuid) in set_values:
            new_entry = DocumentFile(documentid=base_doc.id, hash=hash, remotefileuuid=remotefileuuid)
            try:
                num_new_rows = new_entry.save(force_insert=True)
                assert num_new_rows > 0, colored("ERROR: No row was created", 'red')
            except IntegrityError:
                print(colored('ERROR: Entry already exists', 'red'))

        # Combine fields in equivalent Document entries
        for field in fields_of_interest:
            values = [getattr(doc, field) for doc in query]
            values = [x for x in values if x is not None]
            if values:
                set_values = set(values)
            else:
                set_values = {None}

            if len(set_values) > 1:
                if field in conflict_solver:
                    value = conflict_solver[field](values)
                else:
                    print(colored("ERROR: conflicting %s" % field, 'red'), *set_values, sep='\n')
                    value = input("Give manual value: ")
                    # TODO: Fix by hand via input?
            else:
                # Keep single element from set unpacking
                (value,) = set_values
            setattr(base_doc, field, value)

        print(colored("Rewriting values in doc id %s" % base_doc.id, 'yellow'))
        num_modified_rows = base_doc.save()
        assert num_modified_rows > 0, colored("ERROR: No row was modified", 'red')

        if do_delete_remaining:
            # Delete redundant rows (skipping base document)
            for doc in query[1:]:
                num_deleted_rows = doc.delete_instance()
                assert num_deleted_rows > 0, "Row was not removed"


def main():
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
    find_duplicates_and_fuse('title', repeated_titles[0])

    # Fuse fields of rows with repeated title into a single row
    for title in repeated_titles:
        query = Document.select().prefetch(Author, Url, Tag).where(Document.title == title)
        print("Fixing %s" % title)
        print("===================")
        fuse_fields(query, do_delete_remaining=do_delete)

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
        fuse_fields(query, do_delete_remaining=do_delete)

    return True

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
    if True:
        for key, entries in docs_by_key.items():
            print("Citation key: " + key)
            for entry in entries:
                print("{id}:\t{citationkey} -> {title}".format(**entry))

    return True


if __name__ == '__main__':
    main()
