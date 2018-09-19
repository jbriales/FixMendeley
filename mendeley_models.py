from peewee import *

database = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Canonicaldocuments(BaseModel):
    catalogurl = UnknownField(db_column='catalogUrl', null=True)  # VARCHAR
    downloadurl = UnknownField(db_column='downloadUrl', null=True)  # VARCHAR
    lastmodified = IntegerField(db_column='lastModified')
    uuid = UnknownField(unique=True)  # VARCHAR

    class Meta:
        db_table = 'CanonicalDocuments'

class Datacleaner(BaseModel):
    version = IntegerField()

    class Meta:
        db_table = 'DataCleaner'
        primary_key = False

class Documentcanonicalids(BaseModel):
    canonicalid = IntegerField(db_column='canonicalId', index=True)
    documentid = PrimaryKeyField(db_column='documentId', null=True)
    timestamp = IntegerField()

    class Meta:
        db_table = 'DocumentCanonicalIds'

class Documentcontributors(BaseModel):
    contribution = UnknownField()  # VARCHAR
    documentid = IntegerField(db_column='documentId', index=True)
    firstnames = UnknownField(db_column='firstNames', null=True)  # VARCHAR
    lastname = UnknownField(db_column='lastName')  # VARCHAR

    class Meta:
        db_table = 'DocumentContributors'

class Documentdetailsbase(BaseModel):
    conflictvalue = UnknownField(db_column='conflictValue', null=True)  # VARCHAR
    documentid = IntegerField(db_column='documentId', index=True)
    fieldid = IntegerField(db_column='fieldId')
    originalvalue = UnknownField(db_column='originalValue', null=True)  # VARCHAR

    class Meta:
        db_table = 'DocumentDetailsBase'
        indexes = (
            (('documentid', 'fieldid'), True),
        )
        primary_key = CompositeKey('documentid', 'fieldid')

class Documentfields(BaseModel):
    fieldid = PrimaryKeyField(db_column='fieldId', null=True)
    name = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'DocumentFields'

class Documentfiles(BaseModel):
    documentid = IntegerField(db_column='documentId', index=True)
    downloadrestricted = BooleanField(db_column='downloadRestricted')
    hash = UnknownField(index=True)  # CHAR[40]
    remotefileuuid = UnknownField(db_column='remoteFileUuid')  # CHAR[38]
    unlinked = BooleanField()

    class Meta:
        db_table = 'DocumentFiles'
        primary_key = False

class Documentfolders(BaseModel):
    documentid = IntegerField(db_column='documentId')
    folderid = IntegerField(db_column='folderId')
    status = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'DocumentFolders'
        indexes = (
            (('documentid', 'folderid'), True),
        )
        primary_key = CompositeKey('documentid', 'folderid')

class Documentfoldersbase(BaseModel):
    documentid = IntegerField(db_column='documentId', index=True)
    folderid = IntegerField(db_column='folderId')

    class Meta:
        db_table = 'DocumentFoldersBase'
        indexes = (
            (('documentid', 'folderid'), True),
        )
        primary_key = CompositeKey('documentid', 'folderid')

class Documentkeywords(BaseModel):
    documentid = IntegerField(db_column='documentId')
    keyword = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'DocumentKeywords'
        indexes = (
            (('documentid', 'keyword'), True),
        )
        primary_key = CompositeKey('documentid', 'keyword')

class Documents(BaseModel):
    abstract = UnknownField(null=True)  # VARCHAR
    added = IntegerField(null=True)
    advisor = UnknownField(null=True)  # VARCHAR
    applicationnumber = UnknownField(db_column='applicationNumber', null=True)  # VARCHAR
    articlecolumn = UnknownField(db_column='articleColumn', null=True)  # VARCHAR
    arxivid = UnknownField(db_column='arxivId', null=True)  # VARCHAR
    chapter = UnknownField(null=True)  # VARCHAR
    citationkey = UnknownField(db_column='citationKey', null=True)  # VARCHAR
    city = UnknownField(null=True)  # VARCHAR
    code = UnknownField(null=True)  # VARCHAR
    codenumber = UnknownField(db_column='codeNumber', null=True)  # VARCHAR
    codesection = UnknownField(db_column='codeSection', null=True)  # VARCHAR
    codevolume = UnknownField(db_column='codeVolume', null=True)  # VARCHAR
    committee = UnknownField(null=True)  # VARCHAR
    confirmed = IntegerField(null=True)
    counsel = UnknownField(null=True)  # VARCHAR
    country = UnknownField(null=True)  # VARCHAR
    dateaccessed = UnknownField(db_column='dateAccessed', null=True)  # VARCHAR
    day = IntegerField(null=True)
    deduplicated = IntegerField(null=True)
    deletionpending = IntegerField(db_column='deletionPending', null=True)
    department = UnknownField(null=True)  # VARCHAR
    doi = UnknownField(null=True)  # VARCHAR
    edition = UnknownField(null=True)  # VARCHAR
    favourite = IntegerField(null=True)
    genre = UnknownField(null=True)  # VARCHAR
    hidefrommendeleywebindex = IntegerField(db_column='hideFromMendeleyWebIndex', null=True)
    importer = UnknownField(null=True)  # VARCHAR
    institution = UnknownField(null=True)  # VARCHAR
    internationalauthor = UnknownField(db_column='internationalAuthor', null=True)  # VARCHAR
    internationalnumber = UnknownField(db_column='internationalNumber', null=True)  # VARCHAR
    internationaltitle = UnknownField(db_column='internationalTitle', null=True)  # VARCHAR
    internationalusertype = UnknownField(db_column='internationalUserType', null=True)  # VARCHAR
    isbn = UnknownField(null=True)  # VARCHAR
    issn = UnknownField(null=True)  # VARCHAR
    issue = UnknownField(null=True)  # VARCHAR
    language = UnknownField(null=True)  # VARCHAR
    lastupdate = UnknownField(db_column='lastUpdate', null=True)  # VARCHAR
    legalstatus = UnknownField(db_column='legalStatus', null=True)  # VARCHAR
    length = UnknownField(null=True)  # VARCHAR
    medium = UnknownField(null=True)  # VARCHAR
    modified = IntegerField(null=True)
    month = IntegerField(null=True)
    note = UnknownField(null=True)  # VARCHAR
    originalpublication = UnknownField(db_column='originalPublication', null=True)  # VARCHAR
    owner = UnknownField(null=True)  # VARCHAR
    pages = UnknownField(null=True)  # VARCHAR
    pmid = BigIntegerField(null=True)
    privacy = UnknownField(null=True)  # VARCHAR
    publiclawnumber = UnknownField(db_column='publicLawNumber', null=True)  # VARCHAR
    publication = UnknownField(null=True)  # VARCHAR
    publisher = UnknownField(null=True)  # VARCHAR
    read = IntegerField(null=True)
    reprintedition = UnknownField(db_column='reprintEdition', null=True)  # VARCHAR
    reviewedarticle = UnknownField(db_column='reviewedArticle', null=True)  # VARCHAR
    revisionnumber = UnknownField(db_column='revisionNumber', null=True)  # VARCHAR
    sections = UnknownField(null=True)  # VARCHAR
    series = UnknownField(null=True)  # VARCHAR
    serieseditor = UnknownField(db_column='seriesEditor', null=True)  # VARCHAR
    seriesnumber = UnknownField(db_column='seriesNumber', null=True)  # VARCHAR
    session = UnknownField(null=True)  # VARCHAR
    shorttitle = UnknownField(db_column='shortTitle', null=True)  # VARCHAR
    sourcetype = UnknownField(db_column='sourceType', null=True)  # VARCHAR
    title = UnknownField(null=True)  # VARCHAR
    type = UnknownField(null=True)  # VARCHAR
    usertype = UnknownField(db_column='userType', null=True)  # VARCHAR
    uuid = UnknownField(unique=True)  # VARCHAR
    volume = UnknownField(null=True)  # VARCHAR
    year = IntegerField(null=True)

    class Meta:
        db_table = 'Documents'

class Documentnotes(BaseModel):
    basenote = UnknownField(db_column='baseNote', null=True)  # VARCHAR
    documentid = ForeignKeyField(db_column='documentId', rel_model=Documents, to_field='id', unique=True)
    text = UnknownField()  # VARCHAR
    unlinked = BooleanField()
    uuid = UnknownField(unique=True)  # CHAR[38]

    class Meta:
        db_table = 'DocumentNotes'

class Documentreferences(BaseModel):
    documentid = IntegerField(db_column='documentId', index=True)
    referenceddocumentid = IntegerField(db_column='referencedDocumentId', index=True)

    class Meta:
        db_table = 'DocumentReferences'
        indexes = (
            (('documentid', 'referenceddocumentid'), True),
        )
        primary_key = CompositeKey('documentid', 'referenceddocumentid')

class Documenttags(BaseModel):
    documentid = IntegerField(db_column='documentId')
    tag = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'DocumentTags'
        indexes = (
            (('documentid', 'tag'), True),
        )
        primary_key = CompositeKey('documentid', 'tag')

class Documenturls(BaseModel):
    documentid = IntegerField(db_column='documentId')
    position = IntegerField()
    url = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'DocumentUrls'
        indexes = (
            (('documentid', 'position'), True),
        )
        primary_key = CompositeKey('documentid', 'position')

class Documentversion(BaseModel):
    documentid = PrimaryKeyField(db_column='documentId', null=True)
    version = UnknownField(null=True)  # VARCHAR

    class Meta:
        db_table = 'DocumentVersion'

class Documentzotero(BaseModel):
    documentid = PrimaryKeyField(db_column='documentId', null=True)
    lastsynctime = IntegerField(db_column='lastSyncTime')
    zoteroid = IntegerField(db_column='zoteroID')

    class Meta:
        db_table = 'DocumentZotero'

class Eventlog(BaseModel):
    sent = BooleanField()
    timestamp = IntegerField()
    type = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'EventLog'

class Eventattributes(BaseModel):
    attribute = UnknownField()  # VARCHAR
    eventid = ForeignKeyField(db_column='eventId', null=True, rel_model=Eventlog, to_field='id')
    value = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'EventAttributes'
        indexes = (
            (('eventid', 'attribute'), True),
        )
        primary_key = CompositeKey('attribute', 'eventid')

class Filehighlights(BaseModel):
    author = UnknownField(null=True)  # VARCHAR
    color = UnknownField(null=True)  # VARCHAR
    createdtime = UnknownField(db_column='createdTime')  # VARCHAR
    documentid = ForeignKeyField(db_column='documentId', rel_model=Documents, to_field='id')
    filehash = UnknownField(db_column='fileHash', index=True)  # CHAR[40]
    profileuuid = UnknownField(db_column='profileUuid', null=True)  # VARCHAR
    unlinked = BooleanField()
    uuid = UnknownField(unique=True)  # CHAR[38]

    class Meta:
        db_table = 'FileHighlights'

class Filehighlightrects(BaseModel):
    highlightid = ForeignKeyField(db_column='highlightId', rel_model=Filehighlights, to_field='id')
    page = IntegerField()
    x1 = UnknownField()  # FLOAT
    x2 = UnknownField()  # FLOAT
    y1 = UnknownField()  # FLOAT
    y2 = UnknownField()  # FLOAT

    class Meta:
        db_table = 'FileHighlightRects'

class Filenotes(BaseModel):
    author = UnknownField(null=True)  # VARCHAR
    basenote = UnknownField(db_column='baseNote', null=True)  # VARCHAR
    color = UnknownField(null=True)  # VARCHAR
    createdtime = UnknownField(db_column='createdTime')  # VARCHAR
    documentid = ForeignKeyField(db_column='documentId', rel_model=Documents, to_field='id')
    filehash = UnknownField(db_column='fileHash', index=True)  # CHAR[40]
    modifiedtime = UnknownField(db_column='modifiedTime')  # VARCHAR
    note = UnknownField()  # VARCHAR
    page = IntegerField()
    profileuuid = UnknownField(db_column='profileUuid', null=True)  # VARCHAR
    unlinked = BooleanField()
    uuid = UnknownField(unique=True)  # CHAR[38]
    x = UnknownField()  # FLOAT
    y = UnknownField()  # FLOAT

    class Meta:
        db_table = 'FileNotes'

class Fileviewstates(BaseModel):
    hash = UnknownField(null=True, primary_key=True)  # CHAR[40]
    pagenumber = IntegerField()
    positionx = UnknownField()  # FLOAT
    positiony = UnknownField()  # FLOAT
    rotation = UnknownField()  # FLOAT
    zoomfactor = UnknownField()  # FLOAT
    zoommode = IntegerField()

    class Meta:
        db_table = 'FileViewStates'

class Files(BaseModel):
    hash = UnknownField(null=True, primary_key=True)  # CHAR[40]
    localurl = UnknownField(db_column='localUrl')  # VARCHAR

    class Meta:
        db_table = 'Files'

class Folders(BaseModel):
    access = UnknownField()  # VARCHAR
    creatorname = UnknownField(db_column='creatorName', null=True)  # VARCHAR
    creatorprofileurl = UnknownField(db_column='creatorProfileUrl', null=True)  # VARCHAR
    description = UnknownField(null=True)  # VARCHAR
    downloadfilespolicy = IntegerField(db_column='downloadFilesPolicy')
    name = UnknownField()  # VARCHAR
    parentid = IntegerField(db_column='parentId', null=True)
    publicurl = UnknownField(db_column='publicUrl', null=True)  # VARCHAR
    syncpolicy = UnknownField(db_column='syncPolicy')  # VARCHAR
    uploadfilespolicy = IntegerField(db_column='uploadFilesPolicy')
    uuid = UnknownField(null=True, unique=True)  # VARCHAR

    class Meta:
        db_table = 'Folders'

class Groups(BaseModel):
    access = UnknownField()  # VARCHAR
    downloadfilespolicy = IntegerField(db_column='downloadFilesPolicy')
    grouptype = UnknownField(db_column='groupType')  # VARCHAR
    iconname = UnknownField(db_column='iconName', null=True)  # VARCHAR
    isowner = BooleanField(db_column='isOwner')
    isprivate = BooleanField(db_column='isPrivate')
    isreadonly = BooleanField(db_column='isReadOnly')
    name = UnknownField(null=True)  # VARCHAR
    publicurl = UnknownField(db_column='publicUrl', null=True)  # VARCHAR
    remoteid = IntegerField(db_column='remoteId', null=True)
    remoteuuid = UnknownField(db_column='remoteUuid', null=True, unique=True)  # VARCHAR
    status = UnknownField()  # VARCHAR
    syncpolicy = UnknownField(db_column='syncPolicy')  # VARCHAR
    uploadfilespolicy = IntegerField(db_column='uploadFilesPolicy')

    class Meta:
        db_table = 'Groups'

class Htmllocalstorage(BaseModel):
    key = UnknownField()  # VARCHAR
    origin = UnknownField()  # VARCHAR
    value = UnknownField(null=True)  # VARCHAR

    class Meta:
        db_table = 'HtmlLocalStorage'
        indexes = (
            (('origin', 'key'), True),
        )
        primary_key = CompositeKey('key', 'origin')

class Importhistory(BaseModel):
    ignore = BooleanField()
    importcount = IntegerField(db_column='importCount')
    path = UnknownField(primary_key=True)  # VARCHAR

    class Meta:
        db_table = 'ImportHistory'

class Lastreadstates(BaseModel):
    documentid = ForeignKeyField(db_column='documentId', rel_model=Documents, to_field='id')
    hash = UnknownField()  # VARCHAR
    horizontalposition = UnknownField(db_column='horizontalPosition', null=True)  # FLOAT
    page = IntegerField()
    rotation = IntegerField(null=True)
    status = UnknownField(null=True)  # VARCHAR
    timestamp = UnknownField(null=True)  # VARCHAR
    verticalposition = UnknownField(db_column='verticalPosition')  # FLOAT
    zoomfactor = UnknownField(db_column='zoomFactor', null=True)  # FLOAT
    zoommode = IntegerField(db_column='zoomMode', null=True)

    class Meta:
        db_table = 'LastReadStates'
        indexes = (
            (('documentid', 'hash'), True),
        )
        primary_key = CompositeKey('documentid', 'hash')

class Notduplicates(BaseModel):
    uuid1 = UnknownField()  # CHAR[64]
    uuid2 = UnknownField()  # CHAR[64]

    class Meta:
        db_table = 'NotDuplicates'
        indexes = (
            (('uuid1', 'uuid2'), True),
        )
        primary_key = CompositeKey('uuid1', 'uuid2')

class Profiles(BaseModel):
    clientdata = TextField(db_column='clientData', null=True)
    displayname = UnknownField(db_column='displayName', null=True)  # VARCHAR
    firstname = UnknownField(db_column='firstName', null=True)  # VARCHAR
    isself = IntegerField(db_column='isSelf')
    lastname = UnknownField(db_column='lastName', null=True)  # VARCHAR
    lastsync = TextField(null=True)
    link = UnknownField(null=True)  # VARCHAR
    photo = BlobField(null=True)
    uuid = UnknownField(primary_key=True)  # VARCHAR

    class Meta:
        db_table = 'Profiles'

class Remotedocumentnotes(BaseModel):
    revision = IntegerField()
    status = UnknownField()  # VARCHAR
    uuid = UnknownField(null=True, primary_key=True)  # CHAR[38]

    class Meta:
        db_table = 'RemoteDocumentNotes'

class Remotedocuments(BaseModel):
    documentid = IntegerField(db_column='documentId', index=True, null=True)
    groupid = IntegerField(db_column='groupId')
    intrash = BooleanField(db_column='inTrash')
    remoteid = IntegerField(db_column='remoteId', null=True)
    remoteuuid = UnknownField(db_column='remoteUuid', null=True, unique=True)  # VARCHAR
    status = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'RemoteDocuments'
        indexes = (
            (('documentid', 'remoteuuid'), True),
        )
        primary_key = CompositeKey('documentid', 'remoteuuid')

class Remotefilehighlights(BaseModel):
    revision = IntegerField()
    status = UnknownField()  # VARCHAR
    uuid = UnknownField(null=True, primary_key=True)  # CHAR[38]

    class Meta:
        db_table = 'RemoteFileHighlights'

class Remotefilenotes(BaseModel):
    revision = IntegerField()
    status = UnknownField()  # VARCHAR
    uuid = UnknownField(null=True, primary_key=True)  # CHAR[38]

    class Meta:
        db_table = 'RemoteFileNotes'

class Remotefolders(BaseModel):
    folderid = PrimaryKeyField(db_column='folderId', null=True)
    groupid = IntegerField(db_column='groupId', null=True)
    parentremoteid = IntegerField(db_column='parentRemoteId', null=True)
    remoteid = IntegerField(db_column='remoteId', null=True)
    remoteuuid = UnknownField(db_column='remoteUuid', null=True, unique=True)  # VARCHAR
    status = UnknownField()  # VARCHAR
    version = IntegerField()

    class Meta:
        db_table = 'RemoteFolders'

class Resources(BaseModel):
    icondata = BlobField(db_column='iconData', null=True)
    id = UnknownField(null=True, primary_key=True)  # VARCHAR
    type = UnknownField()  # VARCHAR

    class Meta:
        db_table = 'Resources'

class Runssincelastcleanup(BaseModel):
    time = DateTimeField()

    class Meta:
        db_table = 'RunsSinceLastCleanup'
        primary_key = False

class Schemaversion(BaseModel):
    key = UnknownField(null=True, primary_key=True)  # VARCHAR
    value = IntegerField()

    class Meta:
        db_table = 'SchemaVersion'

class Settings(BaseModel):
    key = UnknownField(primary_key=True)  # VARCHAR
    value = UnknownField(null=True)  # 

    class Meta:
        db_table = 'Settings'

class Stats(BaseModel):
    action = CharField(db_column='Action', primary_key=True)
    counter = IntegerField(db_column='Counter')

    class Meta:
        db_table = 'Stats'

class Synctokens(BaseModel):
    groupid = IntegerField(db_column='groupId', index=True)
    token = UnknownField()  # VARCHAR
    type = UnknownField(index=True)  # VARCHAR

    class Meta:
        db_table = 'SyncTokens'
        indexes = (
            (('groupid', 'type'), True),
        )
        primary_key = CompositeKey('groupid', 'type')

class Zoterolastsync(BaseModel):
    time = IntegerField()

    class Meta:
        db_table = 'ZoteroLastSync'
        primary_key = False

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'
        primary_key = False

