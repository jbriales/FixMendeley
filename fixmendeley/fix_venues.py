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

    print(venues)

    # For each conference/journal registered in our dictionary

    # Query for rows using ordered keywords

    # Set field with normalized value for all fields
    pass
