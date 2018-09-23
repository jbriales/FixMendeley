#!/usr/bin/env python3
# coding=utf-8
"""
Explore and fix different Mendeley database issues
"""

from termcolor import colored

from my_mendeley_models import *
# from .scripts.pwizmodels2mymodels import fields_of_interest

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})
# DEBUG: Print all queries to stderr.
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


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


def main():
    # Organize docs into a dictionary by citation key to find conflicts
    docs_by_key = dict()

    # # Find repeated keys and group docs together
    # query = Document.select(fn.myfun(Document)).prefetch(Author, Url, Tag).group_by(Document.citationkey)
    # with db.atomic():
    #     for elem in query:
    #         print("Sth")

    # Fix documents with repeated keys
    citation_key = 'Kanatani1988'
    query = Document.select().prefetch(Author, Url, Tag).where(Document.citationkey == citation_key)
    with db.atomic():
        # Create new doc that gathers all available information (if not conflicting)
        # base_doc = Document()
        # base_doc.citationkey = citation_key
        # Use first doc in the query as base (to keep non-trivial fields already populated)
        # base_doc = query.first()
        base_doc = query[0]
        base_doc.importer = 'PythonImporter'

        # Gather all URLs
        set_urls = set()
        for doc in query:
            print("id %s" % doc.id)
            for url in doc.urls:
                print("- {}: {}".format(url.position, url.url))
                set_urls.add(url.url)
                # TODO: Delete this (will be created again later)
        # Create new URLs linked to base document
        print(colored("Creating DocumentUrls entries for doc <%s>" % base_doc.id, 'yellow'))
        for idx, url in enumerate(set_urls):
            print('%s %s' % (idx, url))
            new_url = Url(documentid=base_doc.id, position=idx, url=url)
            try:
                num_new_urls = new_url.save(force_insert=True)
            except IntegrityError:
                print(colored('ERROR: Entry already exists', 'red'))

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
