#!/usr/bin/env python3
# coding=utf-8
"""
Take text file with pwiz output and fix some buggy fields
E.g.
Turns 'abstract = UnknownField(null=True) # VARCHAR'
into 'abstract = CharField(null=True)'
"""

import re


fields_of_interest = [
    'title',
    'type',
    'abstract',
    'added',
    'modified',
    'importer',
    'arxivid',
    'citationkey',
    'city',
    'country',
    'dateaccessed',
    'doi',
    'institution',
    'month',
    'pages',
    'volume',
    'year',
    'publication',
    'sourcetype'
]

def main():
    with open('pwizmodels.txt', 'r') as f:
        # Create regex pattern matcher
        # Example:
        # abstract = UnknownField(null=True) # VARCHAR
        pattern_groups = dict()
        pattern_groups['varname'] = '(?P<varname>\w+)'
        pattern_groups['command'] = '(?P<command>\w+)'
        pattern_groups['args'] = '(?P<args>.*)'
        pattern_groups['comment'] = '(?P<comment>\w+)'
        pattern_str = '{varname} = {command}\({args}\)\s*(# {comment})*'.format(**pattern_groups)
        r = re.compile(pattern_str)

        lines = f.read().strip().split('\n')
        for line in lines:
            out = r.match(line)
            if out is None:
                print("ERROR: Bad parsing of %s" % line)
                continue
            parsed_values = out.groupdict()

            if parsed_values['varname'] not in fields_of_interest:
                continue

            # Convert this into right line
            if not parsed_values['comment']:
                print(line)
            else:
                if parsed_values['comment'] == 'VARCHAR':
                    parsed_values['command'] = 'CharField'
                    print('{varname} = {command}({args})'.format(**parsed_values))
                else:
                    # Keep as it was
                    print(line)

    return True


if __name__ == '__main__':
    main()
