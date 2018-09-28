# coding=utf-8
"""
Fix Mendeley database entries via query from DBLP
"""

import json
from pkg_resources import resource_filename
import re
import requests
from termcolor import colored
import urllib.request

import bibtexparser
from peewee import SqliteDatabase
from fixmendeley.my_mendeley_models import *

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})

DBLP_BASE_URL = 'http://dblp.org/search/publ/api?'
DBLP_QUERY_URL = DBLP_BASE_URL + 'q={title}&format=json'


def query_dblp(title):
    # Remove special characters from title
    title = re.sub(r'[:∗⋆]', '', title)
    query_url = DBLP_QUERY_URL.format(title=title)
    try:
        resp = requests.get(query_url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print(colored("ERROR in URL syntax:\n%s" % query_url, 'red'))
        raise Exception('URL Syntax')

    resp_hits = json.loads(resp.text)['result']['hits']
    if int(resp_hits['@total']) == 0:
        return None
    else:
        return resp_hits['hit']


def choose_dblp_info(db_entry, hits):
    if len(hits) == 1:
        return hits[0]['info']
    else:
        # Is there an exact title match?
        title = db_entry.title
        remove_list = r':∗⋆.\- \n'
        title_lowernospace = re.sub(r'[%s]' % remove_list, '', title.lower())

        [hit['info']['title'] for hit in hits]
        for hit in hits:
            info_ = hit['info']
            info_title = re.sub(r'[%s]' % remove_list, '', info_['title'].lower())
            if info_title == title_lowernospace:
                # "Exact" match
                return info_

        raise Exception("Choosing dblp, no exact match")


def import_dblp(do_write_authors=False, do_force_all=False):
    """
    Fix all main fields of Mendeley database entries via query from dblp by title
    :rtype: object
    """

    # Query all Mendeley documents corresponding document entry from Mendeley database
    if do_force_all:
        query = Document.select().prefetch(Author, Url)
    else:
        # Skip those already imported from dblp
        query = Document.select().prefetch(Author, Url).where(Document.importer != "dblp")

    with db.atomic():
        for db_entry in query:
            entry_str = "{id}: {citationkey} -> {title}".format(**db_entry.__data__)

            if db_entry.type == 'Generic':
                print(colored("WARNING: Skipping generic entry %s" % entry_str, 'yellow'))
                continue

            try:
                hits = query_dblp(db_entry.title)

                if not hits:
                    print(colored("WARNING: {title} not in DBLP".format(**db_entry.__data__), 'yellow'))
                    continue

                # Pick one entry from found dblp hits
                info = choose_dblp_info(db_entry, hits)

                # Get bibtex entry
                bib_url = info['url'] + '.bib'
                response = urllib.request.urlopen(bib_url)
                bib_text = response.read().decode('utf-8')
                # Parse bibtex
                bib_db = bibtexparser.loads(bib_text)
                bib_dict = bib_db.entries[0]

                if info['type'] == 'Conference and Workshop Papers':
                    from .mendeley.documents import Inproceedings
                    doc = Inproceedings()
                    doc.load_dblp(bib_dict, info)
                elif info['type'] == 'Journal Articles':
                    from .mendeley.documents import Article
                    doc = Article()
                    doc.load_dblp(bib_dict, info)
                elif info['type'] == 'Books and Theses':
                    raise Exception('TODO: Implement Book type')
                else:
                    raise Exception('TODO: Unknown type %s' % info['type'])

                if do_write_authors:
                    for author in db_entry.authors:
                        num_deleted_rows = author.delete_instance()
                        assert num_deleted_rows > 0, colored("ERROR: No row was deleted", 'red')

                    for author in doc.authors:
                        # Add new authors
                        Author.create(documentid=db_entry.id,
                                      firstnames=author['firstnames'],
                                      lastname=author['lastname'],
                                      contribution="DocumentAuthor")
                    # TODO: Remove previous authors

                # Drop authors field
                delattr(doc, "authors")

                # Write populated fields in database row
                for key, val in vars(doc).items():
                    setattr(db_entry, key, val)

                # print(colored("Saving %d: %s -> %s" % (base_doc.id, 'yellow'))
                print(colored("Saving %s" % entry_str, 'cyan'))
                num_modified_rows = db_entry.save()
                assert num_modified_rows > 0, colored("ERROR: No row was modified", 'red')

            except Exception as err:
                import sys
                print(colored("\n=================", 'red'))
                print(colored("Error in %s" % entry_str, 'red'))
                # print(colored(*err.args, 'red'))
                import traceback
                print(colored(traceback.format_exc(), 'red'))
                print("Pause")

    return True

    print("Querying from DBLP")
    title = "Lifting 3D Manhattan Lines from a Single Image"
    title = "3D corner detection and matching for manmade scene/object structure cognition"
    title = "Exactness of semidefinite relaxations for nonlinear optimization problems with underlying graph structure"
    # title = "On Differentiating Eigenvalues and Eigenvectors"

    dblp_entry = query_dblp(title)

    # Get corresponding document entry from Mendeley database
    query = (
        Document
        .select()
        .prefetch(Author, Url, Tag)
        .where(Document.title == title)
    )

    for db_entry in query:
        print("Do something here")

    return True
