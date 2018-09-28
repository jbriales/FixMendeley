#!/usr/bin/env python3
# coding=utf-8
"""
Explore and fix different Mendeley database issues
"""

import argparse
import sys

# DEBUG: Print all queries to stderr.
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="By Jesus Briales"
    )
    subparsers = parser.add_subparsers()

    from fixmendeley.fuse_entries import find_duplicates_and_fuse
    find_duplicates_and_fuse.parser = subparsers.add_parser(
        'fuse-entries',
        description=find_duplicates_and_fuse.__doc__)
    find_duplicates_and_fuse.parser.set_defaults(func=find_duplicates_and_fuse)
    find_duplicates_and_fuse.parser.add_argument('field')
    find_duplicates_and_fuse.parser.add_argument('value')
    find_duplicates_and_fuse.parser.add_argument('--do-delete-remaining', '--delete-remaining',
                                                 action='store_true')

    from fixmendeley.fix_venues import fix_venues
    fix_venues.parser = subparsers.add_parser(
        'fix-venues',
        description=fix_venues.__doc__)
    fix_venues.parser.set_defaults(func=fix_venues)

    from fixmendeley.import_dblp import import_dblp
    import_dblp.parser = subparsers.add_parser(
        'import-dblp',
        description=import_dblp.__doc__)
    import_dblp.parser.set_defaults(func=import_dblp)
    import_dblp.parser.add_argument('--do-force-all', '--force-all',
                                    action='store_true')
    import_dblp.parser.add_argument('--do-write-authors', '--write-authors',
                                    action='store_true')

    from fixmendeley.test import test
    test.parser = subparsers.add_parser(
        'test',
        description=test.__doc__)
    test.parser.set_defaults(func=test)

    if len(sys.argv) <= 1:
        parser.print_help()
        return True

    # Parse arguments
    args = parser.parse_args()
    kwargs = vars(args)
    func = kwargs.pop('func')

    # Call function on user arguments
    successful = func(**kwargs)
    sys.exit(0 if successful else 1)


if __name__ == '__main__':
    main()
