# coding=utf-8
"""
Fix entries via query from DBLP
"""

import requests
from pkg_resources import resource_filename
from termcolor import colored

import json
from peewee import SqliteDatabase
from fixmendeley.my_mendeley_models import *

DBLP_BASE_URL = 'http://dblp.org/search/publ/api?'
DBLP_QUERY_URL = DBLP_BASE_URL + 'q={title}&format=json'


def query_dblp(title):
    resp = requests.get(DBLP_QUERY_URL.format(title=title))
    resp.raise_for_status()

    hits = json.loads(resp.text)['result']['hits']
    if int(hits['@total']) == 0:
        return None
    list_hits = json.loads(resp.text)['result']['hits']['hit']
    assert len(list_hits) == 1, "DBLP query produced %d hits" % len(hits)
    return list_hits[0]['info']


def fix_via_dblp():
    """
    Fix all main fields via query from dblp by title
    :rtype: object
    """
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

    for entry in query:
        print("Do something here")

    return True
