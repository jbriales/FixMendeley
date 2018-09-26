# coding=utf-8
"""
Join repeated Mendeley database entries fusing their fields' content
"""

from termcolor import colored

from peewee import SqliteDatabase

from fixmendeley.my_mendeley_models import *
# from .scripts.pwizmodels2mymodels import fields_of_interest

db = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})

# Fields to fuse between different duplicate entries
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


# Helper functions to fix conflicts in different types of fields
def take_longest_string(values):
    return max(values, key=lambda s: len(s))


def fix_title_conflict(values):
    # Turn lowercase
    # Remove punctuation and whitespace
    from string import punctuation, whitespace
    table = str.maketrans(dict.fromkeys(punctuation+whitespace))
    lowercase_set = {
        value.lower().translate(table)
        for value in values}
    if len(lowercase_set) == 1:
        # min since 'A' < 'a'
        return min(values)
        # sum(1 for c in str if c.isupper())
    else:
        print("Titles:", *values, sep='\n')
        raise Exception("Titles are too different")


def fix_type_conflict(values):
    if {x for x in values} == {"ConferenceProceedings", "JournalArticle"}:
        # In most of these conflicts, it's a conference
        return "ConferenceProceedings"
    else:
        raise Exception("Unexpected document type")


conflict_solver = dict()
conflict_solver['added'] = min
conflict_solver['year'] = max  # just fix it anyway, sick of this
conflict_solver['pages'] = take_longest_string
conflict_solver['publisher'] = take_longest_string
conflict_solver['publication'] = take_longest_string
conflict_solver['title'] = fix_title_conflict
conflict_solver['type'] = fix_type_conflict


def find_duplicates_and_fuse(field, value, do_delete_remaining=False):
    """
    Find all entries whose field <field>'s content coincides with <value>
    and fuse their content into a single entry (the first of them)

    This funcions works as a wrapper for fuse_fields that is peewee-agnostic
    :param field:
    :param value:
    :param do_delete_remaining: Remove other duplicate entries after gathering data in a single entry
    """
    query = Document.select().prefetch(Author, Url, Tag).where(getattr(Document, field) == value)
    fuse_fields(query, do_delete_remaining=do_delete_remaining)


def fuse_fields(query, do_delete_remaining=False):
    """
    Fuse fields from several potentially equivalent documents into first one
    :param query: SQL query with list of conflicting/repeated rows
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
        set_authors = set()
        for doc in query:
            set_nums.add(len(doc.authors))
            set_authors.add(tuple((a.firstnames, a.lastname) for a in doc.authors))
        if len(set_nums) != 1:
            print(colored("ERROR for %s -> %s: conflicting lists of authors"
                          % (base_doc.citationkey, base_doc.title), 'red'))
            from pprint import pprint
            pprint(set_authors)
            raise Exception("Conflicting lists of authors")

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
        print(colored("Combining fields for %s -> %s" % (base_doc.citationkey, base_doc.title), 'cyan'))
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
                    print(colored("ERROR for %s -> %s: conflicting %s" % (base_doc.citationkey, base_doc.title, field), 'red'),
                          *set_values, sep='\n')
                    raise Exception("TODO: Non-available conflict solver")
                    value = input("Give manual value: ")
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
