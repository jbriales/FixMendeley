# coding=utf-8
"""
Classes for different document types
"""

import calendar
import json
import re
from termcolor import colored


class Document:
    def __init__(self):
        # List of fields to complete in @inproceedings entry
        self.authors = None
        self.doi = None
        self.importer = None
        self.pages = None
        self.publication = None
        self.title = None
        self.year = None

    def __repr__(self):
        return json.dumps(vars(self), indent=2)

    def load_dblp(self, bib, info):
        self.importer = 'dblp'

        # Map equivalent dictionary keys to class attributes
        for key in vars(self).keys():
            if not getattr(self, key):
                setattr(self, key, bib.get(key))

        self.year = int(info['year'])

        # Parse authors
        self.authors = list()
        for fullname in bib['author'].split(' and\n'):
            *a, b = fullname.split(' ')
            self.authors.append({'firstnames': ' '.join(a), 'lastname': b})


class Article(Document):
    def __init__(self):
        super().__init__()
        # List of fields to complete in @inproceedings entry
        self.issue = None
        self.type = "JournalArticle"
        self.volume = None

    def load_dblp(self, bib, info):
        super().load_dblp(bib, info)

        self.issue = info.get('number', None)
        self.publication = info['venue']


class Inproceedings(Document):
    def __init__(self):
        super().__init__()
        # List of fields to complete in @inproceedings entry
        self.city = None
        self.country = None
        self.day = None
        self.month = None
        self.type = "ConferenceProceedings"

    def load_dblp(self, bib, info):
        super().load_dblp(bib, info)

        # Log booktitle for subsequent format analysis
        singleline_booktitle = re.sub(r'\n', r' ', bib['booktitle'])
        with open('log.booktitle', 'a') as f:
            f.write(singleline_booktitle+'\n')
        # Parse venue info from booktitle
        pattern_dict = {
            'publication': r'(?P<publication>.*)',
            'short': r'(?P<short>.*)',
            'city': r'(?P<city>[\w-]+)',
            'country': r'(?P<country>[\w-]+)',
            'month': r'(?P<month>[\w]+)',
            'day': r'(?P<day>[\w-]+)',
            'year': r'(?P<year>[\w-]+)',
        }
        pattern_str = r"{publication}, {short}, {city}, {country}, {month} {day}, {year}".format(**pattern_dict)
        try:
            res = re.match(pattern_str, singleline_booktitle).groupdict()
        except AttributeError:
            print(colored('ERROR: Parsing booktitle:\n%s' % bib['booktitle'], 'red'))
            raise Exception('re error')
        # TODO: Register short name into config dict for later use?
        from pprint import pprint
        pprint(res)
        res.pop('short')
        # Turn month into number
        res['month'] = list(calendar.month_name).index(res['month'])
        for key, val in res.items():
            setattr(self, key, val)
