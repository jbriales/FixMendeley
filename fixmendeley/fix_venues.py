# coding=utf-8

from pkg_resources import resource_filename
from termcolor import colored

import json
from peewee import SqliteDatabase
from fixmendeley.my_mendeley_models import *


def fix_venues():
    """
    Fix conference and journal names in publication field
    :rtype: object
    """
    print("Fixing publication field")

    # Load our database of venue names and keywords
    with open(resource_filename('fixmendeley', 'venues.json'), 'r') as f:
        venues = json.load(f)

    for venue in venues:
        # Build filter pattern for keywords
        ordered_keywords = venue['keywords'][0] + venue['keywords'][1]
        reverse_keywords = venue['keywords'][1] + venue['keywords'][0]
        pattern_ordered_keywords = '%' + '%'.join(ordered_keywords) + '%'
        pattern_reverse_keywords = '%' + '%'.join(ordered_keywords) + '%'
        pattern_acronym = '*' + venue['acronym'] + '*'

        query = (
            Document
            .select(Document.publication)
            .where((Document.publication ** pattern_ordered_keywords) |
                   (Document.publication ** pattern_reverse_keywords) |
                   (Document.publication % ('*' + venue['acronym'] + '*')) |
                   (Document.doi ** ('%' + venue['acronym'] + '%'))
                   )
        )
        for entry in query:
            print(entry.publication)

        # For each conference/journal registered in our dictionary

        # Query for rows using ordered keywords

        # Set field with normalized value for all fields
    pass
