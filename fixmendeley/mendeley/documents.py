# coding=utf-8
"""
Classes for different document types
"""

import calendar
import json
import re
from termcolor import colored


class Article:
    def __init__(self):
        # List of fields to complete in @inproceedings entry
        self.authors = None
        self.doi = None
        self.importer = None
        self.month = None
        self.pages = None
        self.publication = None
        self.title = None
        self.type = "JournalArticle"
        self.volume = None
        self.year = None

    def load_dblp_info(self, info):
        self.importer = 'dblp'

        # Map equivalent dictionary keys to class attributes
        for key in vars(self).keys():
            if not getattr(self, key):
                setattr(self, key, info.get(key))

        self.publication = info['venue']

        # Parse authors
        self.authors = list()
        for fullname in info['author'].split(' and\n'):
            *a, b = fullname
            self.authors.append({'firstnames': a, 'lastname': b})

        from pprint import pprint; pprint(vars(self))
        print("Check fields here")


class Inproceedings:
    def __init__(self):
        # List of fields to complete in @inproceedings entry
        self.authors = None
        self.city = None
        self.country = None
        self.day = None
        self.doi = None
        self.importer = None
        self.month = None
        self.pages = None
        self.publication = None
        self.title = None
        self.type = "ConferenceProceedings"
        self.year = None

    def __repr__(self):
        return json.dumps(vars(self), indent=2)

    def load_dblp_bib(self, bib_dict):
        self.importer = 'dblp'

        # Map equivalent dictionary keys to class attributes
        for key in vars(self).keys():
            if not getattr(self, key):
                setattr(self, key, bib_dict.get(key))

        # Parse venue info from booktitle
        pattern_dict = {
            'short': r'(?P<short>.*)',
            'city': r'(?P<city>[\w-]+)',
            'country': r'(?P<country>[\w-]+)',
            'month': r'(?P<month>[\w]+)',
            'day': r'(?P<day>[\w-]+)',
            'year': r'(?P<year>[\w-]+)',
        }
        lines = bib_dict['booktitle'].split('\n')
        self.publication = lines[0].rstrip(',')
        pattern_str = r"{short}, {city}, {country}, {month} {day}, {year}".format(**pattern_dict)
        try:
            res = re.match(pattern_str, lines[1]).groupdict()
        except AttributeError:
            print(colored('ERROR: Parsing booktitle:\n%s' % bib_dict['booktitle'], 'red'))
            raise Exception('re error')
        # TODO: Use/store conf shortname somewhere?
        res.pop('short')
        # Turn month into number
        res['month'] = list(calendar.month_name).index(res['month'])
        calendar
        for key, val in res.items():
            setattr(self, key, val)

        # Parse authors
        self.authors = list()
        for fullname in bib_dict['author'].split(' and\n'):
            *a, b = fullname.split(' ')
            self.authors.append({'firstnames': ' '.join(a), 'lastname': b})
