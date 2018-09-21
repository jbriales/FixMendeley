from peewee import *

database = SqliteDatabase('jesusbriales@uma.es@www.mendeley.com.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Canonicaldocuments(BaseModel):
    catalogurl = CharField(column_name='catalogUrl', null=True)
    downloadurl = CharField(column_name='downloadUrl', null=True)
    lastmodified = IntegerField(column_name='lastModified')
    uuid = CharField(unique=True)

    class Meta:
        table_name = 'CanonicalDocuments'

class Datacleaner(BaseModel):
    version = IntegerField()

    class Meta:
        table_name = 'DataCleaner'
        primary_key = False

class Documentcanonicalids(BaseModel):
    canonicalid = IntegerField(column_name='canonicalId', index=True)
    documentid = AutoField(column_name='documentId', null=True)
    timestamp = IntegerField()

    class Meta:
        table_name = 'DocumentCanonicalIds'

class Documentcontributors(BaseModel):
    contribution = CharField()
    documentid = IntegerField(column_name='documentId', index=True)
    firstnames = CharField(column_name='firstNames', null=True)
    lastname = CharField(column_name='lastName')

    class Meta:
        table_name = 'DocumentContributors'

class Documentdetailsbase(BaseModel):
    conflictvalue = CharField(column_name='conflictValue', null=True)
    documentid = IntegerField(column_name='documentId', index=True)
    fieldid = IntegerField(column_name='fieldId')
    originalvalue = CharField(column_name='originalValue', null=True)

    class Meta:
        table_name = 'DocumentDetailsBase'
        indexes = (
            (('documentid', 'fieldid'), True),
        )
        primary_key = CompositeKey('documentid', 'fieldid')

class Documentfields(BaseModel):
    fieldid = AutoField(column_name='fieldId', null=True)
    name = CharField()

    class Meta:
        table_name = 'DocumentFields'

class Documentfiles(BaseModel):
    documentid = IntegerField(column_name='documentId', index=True)
    downloadrestricted = BooleanField(column_name='downloadRestricted', constraints=[SQL("DEFAULT 0")])
    hash = CharField(index=True)
    remotefileuuid = CharField(column_name='remoteFileUuid', constraints=[SQL("DEFAULT ''")])
    unlinked = BooleanField()

    class Meta:
        table_name = 'DocumentFiles'
        primary_key = False

class Documentfolders(BaseModel):
    documentid = IntegerField(column_name='documentId')
    folderid = IntegerField(column_name='folderId')
    status = CharField()

    class Meta:
        table_name = 'DocumentFolders'
        indexes = (
            (('documentid', 'folderid'), True),
        )
        primary_key = CompositeKey('documentid', 'folderid')

class Documentfoldersbase(BaseModel):
    documentid = IntegerField(column_name='documentId', index=True)
    folderid = IntegerField(column_name='folderId')

    class Meta:
        table_name = 'DocumentFoldersBase'
        indexes = (
            (('documentid', 'folderid'), True),
        )
        primary_key = CompositeKey('documentid', 'folderid')

class Documentkeywords(BaseModel):
    documentid = IntegerField(column_name='documentId')
    keyword = CharField()

    class Meta:
        table_name = 'DocumentKeywords'
        indexes = (
            (('documentid', 'keyword'), True),
        )
        primary_key = CompositeKey('documentid', 'keyword')

class Documents(BaseModel):
    abstract = CharField(null=True)
    added = IntegerField(null=True)
    advisor = CharField(null=True)
    applicationnumber = CharField(column_name='applicationNumber', null=True)
    articlecolumn = CharField(column_name='articleColumn', null=True)
    arxivid = CharField(column_name='arxivId', null=True)
    chapter = CharField(null=True)
    citationkey = CharField(column_name='citationKey', null=True)
    city = CharField(null=True)
    code = CharField(null=True)
    codenumber = CharField(column_name='codeNumber', null=True)
    codesection = CharField(column_name='codeSection', null=True)
    codevolume = CharField(column_name='codeVolume', null=True)
    committee = CharField(null=True)
    confirmed = IntegerField(null=True)
    counsel = CharField(null=True)
    country = CharField(null=True)
    dateaccessed = CharField(column_name='dateAccessed', null=True)
    day = IntegerField(null=True)
    deduplicated = IntegerField(null=True)
    deletionpending = IntegerField(column_name='deletionPending', null=True)
    department = CharField(null=True)
    doi = CharField(null=True)
    edition = CharField(null=True)
    favourite = IntegerField(null=True)
    genre = CharField(null=True)
    hidefrommendeleywebindex = IntegerField(column_name='hideFromMendeleyWebIndex', null=True)
    importer = CharField(null=True)
    institution = CharField(null=True)
    internationalauthor = CharField(column_name='internationalAuthor', null=True)
    internationalnumber = CharField(column_name='internationalNumber', null=True)
    internationaltitle = CharField(column_name='internationalTitle', null=True)
    internationalusertype = CharField(column_name='internationalUserType', null=True)
    isbn = CharField(null=True)
    issn = CharField(null=True)
    issue = CharField(null=True)
    language = CharField(null=True)
    lastupdate = CharField(column_name='lastUpdate', null=True)
    legalstatus = CharField(column_name='legalStatus', null=True)
    length = CharField(null=True)
    medium = CharField(null=True)
    modified = IntegerField(null=True)
    month = IntegerField(null=True)
    note = CharField(null=True)
    originalpublication = CharField(column_name='originalPublication', null=True)
    owner = CharField(null=True)
    pages = CharField(null=True)
    pmid = BigIntegerField(null=True)
    privacy = CharField(null=True)
    publiclawnumber = CharField(column_name='publicLawNumber', null=True)
    publication = CharField(null=True)
    publisher = CharField(null=True)
    read = IntegerField(null=True)
    reprintedition = CharField(column_name='reprintEdition', null=True)
    reviewedarticle = CharField(column_name='reviewedArticle', null=True)
    revisionnumber = CharField(column_name='revisionNumber', null=True)
    sections = CharField(null=True)
    series = CharField(null=True)
    serieseditor = CharField(column_name='seriesEditor', null=True)
    seriesnumber = CharField(column_name='seriesNumber', null=True)
    session = CharField(null=True)
    shorttitle = CharField(column_name='shortTitle', null=True)
    sourcetype = CharField(column_name='sourceType', null=True)
    title = CharField(null=True)
    type = CharField(null=True)
    usertype = CharField(column_name='userType', null=True)
    uuid = CharField(unique=True)
    volume = CharField(null=True)
    year = IntegerField(null=True)

    class Meta:
        table_name = 'Documents'

class Documentnotes(BaseModel):
    basenote = CharField(column_name='baseNote', null=True)
    documentid = ForeignKeyField(column_name='documentId', field='id', model=Documents, unique=True)
    text = CharField()
    unlinked = BooleanField()
    uuid = CharField(unique=True)

    class Meta:
        table_name = 'DocumentNotes'

class Documentreferences(BaseModel):
    documentid = IntegerField(column_name='documentId', index=True)
    referenceddocumentid = IntegerField(column_name='referencedDocumentId', index=True)

    class Meta:
        table_name = 'DocumentReferences'
        indexes = (
            (('documentid', 'referenceddocumentid'), True),
        )
        primary_key = CompositeKey('documentid', 'referenceddocumentid')

class Documenttags(BaseModel):
    documentid = IntegerField(column_name='documentId')
    tag = CharField()

    class Meta:
        table_name = 'DocumentTags'
        indexes = (
            (('documentid', 'tag'), True),
        )
        primary_key = CompositeKey('documentid', 'tag')

class Documenturls(BaseModel):
    documentid = IntegerField(column_name='documentId')
    position = IntegerField()
    url = CharField()

    class Meta:
        table_name = 'DocumentUrls'
        indexes = (
            (('documentid', 'position'), True),
        )
        primary_key = CompositeKey('documentid', 'position')

class Documentversion(BaseModel):
    documentid = AutoField(column_name='documentId', null=True)
    version = CharField(null=True)

    class Meta:
        table_name = 'DocumentVersion'

class Documentzotero(BaseModel):
    documentid = AutoField(column_name='documentId', null=True)
    lastsynctime = IntegerField(column_name='lastSyncTime')
    zoteroid = IntegerField(column_name='zoteroID')

    class Meta:
        table_name = 'DocumentZotero'

class Eventlog(BaseModel):
    sent = BooleanField()
    timestamp = IntegerField()
    type = CharField()

    class Meta:
        table_name = 'EventLog'

class Eventattributes(BaseModel):
    attribute = CharField()
    eventid = ForeignKeyField(column_name='eventId', field='id', model=Eventlog, null=True)
    value = CharField()

    class Meta:
        table_name = 'EventAttributes'
        indexes = (
            (('eventid', 'attribute'), True),
        )
        primary_key = CompositeKey('attribute', 'eventid')

class Filehighlights(BaseModel):
    author = CharField(null=True)
    color = CharField(null=True)
    createdtime = CharField(column_name='createdTime')
    documentid = ForeignKeyField(column_name='documentId', field='id', model=Documents)
    filehash = CharField(column_name='fileHash', index=True)
    profileuuid = CharField(column_name='profileUuid', null=True)
    unlinked = BooleanField()
    uuid = CharField(unique=True)

    class Meta:
        table_name = 'FileHighlights'

class Filehighlightrects(BaseModel):
    highlightid = ForeignKeyField(column_name='highlightId', field='id', model=Filehighlights)
    page = IntegerField()
    x1 = FloatField()
    x2 = FloatField()
    y1 = FloatField()
    y2 = FloatField()

    class Meta:
        table_name = 'FileHighlightRects'

class Filenotes(BaseModel):
    author = CharField(null=True)
    basenote = CharField(column_name='baseNote', null=True)
    color = CharField(null=True)
    createdtime = CharField(column_name='createdTime')
    documentid = ForeignKeyField(column_name='documentId', field='id', model=Documents)
    filehash = CharField(column_name='fileHash', index=True)
    modifiedtime = CharField(column_name='modifiedTime')
    note = CharField()
    page = IntegerField()
    profileuuid = CharField(column_name='profileUuid', null=True)
    unlinked = BooleanField()
    uuid = CharField(unique=True)
    x = FloatField()
    y = FloatField()

    class Meta:
        table_name = 'FileNotes'

class Fileviewstates(BaseModel):
    hash = CharField(null=True, primary_key=True)
    pagenumber = IntegerField()
    positionx = FloatField()
    positiony = FloatField()
    rotation = FloatField()
    zoomfactor = FloatField()
    zoommode = IntegerField()

    class Meta:
        table_name = 'FileViewStates'

class Files(BaseModel):
    hash = CharField(null=True, primary_key=True)
    localurl = CharField(column_name='localUrl')

    class Meta:
        table_name = 'Files'

class Folders(BaseModel):
    access = CharField()
    creatorname = CharField(column_name='creatorName', null=True)
    creatorprofileurl = CharField(column_name='creatorProfileUrl', null=True)
    description = CharField(null=True)
    downloadfilespolicy = IntegerField(column_name='downloadFilesPolicy')
    name = CharField()
    parentid = IntegerField(column_name='parentId', null=True)
    publicurl = CharField(column_name='publicUrl', null=True)
    syncpolicy = CharField(column_name='syncPolicy')
    uploadfilespolicy = IntegerField(column_name='uploadFilesPolicy')
    uuid = CharField(null=True, unique=True)

    class Meta:
        table_name = 'Folders'

class Groups(BaseModel):
    access = CharField()
    downloadfilespolicy = IntegerField(column_name='downloadFilesPolicy')
    grouptype = CharField(column_name='groupType')
    iconname = CharField(column_name='iconName', null=True)
    isowner = BooleanField(column_name='isOwner')
    isprivate = BooleanField(column_name='isPrivate')
    isreadonly = BooleanField(column_name='isReadOnly')
    name = CharField(null=True)
    publicurl = CharField(column_name='publicUrl', null=True)
    remoteid = IntegerField(column_name='remoteId', null=True)
    remoteuuid = CharField(column_name='remoteUuid', null=True, unique=True)
    status = CharField()
    syncpolicy = CharField(column_name='syncPolicy')
    uploadfilespolicy = IntegerField(column_name='uploadFilesPolicy')

    class Meta:
        table_name = 'Groups'

class Htmllocalstorage(BaseModel):
    key = CharField()
    origin = CharField()
    value = CharField(null=True)

    class Meta:
        table_name = 'HtmlLocalStorage'
        indexes = (
            (('origin', 'key'), True),
        )
        primary_key = CompositeKey('key', 'origin')

class Importhistory(BaseModel):
    ignore = BooleanField()
    importcount = IntegerField(column_name='importCount')
    path = CharField(primary_key=True)

    class Meta:
        table_name = 'ImportHistory'

class Lastreadstates(BaseModel):
    documentid = ForeignKeyField(column_name='documentId', field='id', model=Documents)
    hash = CharField()
    horizontalposition = FloatField(column_name='horizontalPosition', null=True)
    page = IntegerField()
    rotation = IntegerField(null=True)
    status = CharField(null=True)
    timestamp = CharField(null=True)
    verticalposition = FloatField(column_name='verticalPosition')
    zoomfactor = FloatField(column_name='zoomFactor', null=True)
    zoommode = IntegerField(column_name='zoomMode', null=True)

    class Meta:
        table_name = 'LastReadStates'
        indexes = (
            (('documentid', 'hash'), True),
        )
        primary_key = CompositeKey('documentid', 'hash')

class Notduplicates(BaseModel):
    uuid1 = CharField()
    uuid2 = CharField()

    class Meta:
        table_name = 'NotDuplicates'
        indexes = (
            (('uuid1', 'uuid2'), True),
        )
        primary_key = CompositeKey('uuid1', 'uuid2')

class Profiles(BaseModel):
    clientdata = TextField(column_name='clientData', null=True)
    displayname = CharField(column_name='displayName', null=True)
    firstname = CharField(column_name='firstName', null=True)
    isself = IntegerField(column_name='isSelf')
    lastname = CharField(column_name='lastName', null=True)
    lastsync = TextField(null=True)
    link = CharField(null=True)
    photo = BlobField(null=True)
    uuid = CharField(primary_key=True)

    class Meta:
        table_name = 'Profiles'

class Remotedocumentnotes(BaseModel):
    revision = IntegerField()
    status = CharField()
    uuid = CharField(null=True, primary_key=True)

    class Meta:
        table_name = 'RemoteDocumentNotes'

class Remotedocuments(BaseModel):
    documentid = IntegerField(column_name='documentId', index=True, null=True)
    groupid = IntegerField(column_name='groupId')
    intrash = BooleanField(column_name='inTrash')
    remoteid = IntegerField(column_name='remoteId', null=True)
    remoteuuid = CharField(column_name='remoteUuid', null=True, unique=True)
    status = CharField()

    class Meta:
        table_name = 'RemoteDocuments'
        indexes = (
            (('documentid', 'remoteuuid'), True),
        )
        primary_key = CompositeKey('documentid', 'remoteuuid')

class Remotefilehighlights(BaseModel):
    revision = IntegerField()
    status = CharField()
    uuid = CharField(null=True, primary_key=True)

    class Meta:
        table_name = 'RemoteFileHighlights'

class Remotefilenotes(BaseModel):
    revision = IntegerField()
    status = CharField()
    uuid = CharField(null=True, primary_key=True)

    class Meta:
        table_name = 'RemoteFileNotes'

class Remotefolders(BaseModel):
    folderid = AutoField(column_name='folderId', null=True)
    groupid = IntegerField(column_name='groupId', null=True)
    parentremoteid = IntegerField(column_name='parentRemoteId', null=True)
    remoteid = IntegerField(column_name='remoteId', null=True)
    remoteuuid = CharField(column_name='remoteUuid', null=True, unique=True)
    status = CharField()
    version = IntegerField()

    class Meta:
        table_name = 'RemoteFolders'

class Resources(BaseModel):
    icondata = BlobField(column_name='iconData', null=True)
    id = CharField(null=True, primary_key=True)
    type = CharField()

    class Meta:
        table_name = 'Resources'

class Runssincelastcleanup(BaseModel):
    time = DateTimeField()

    class Meta:
        table_name = 'RunsSinceLastCleanup'
        primary_key = False

class Schemaversion(BaseModel):
    key = CharField(null=True, primary_key=True)
    value = IntegerField()

    class Meta:
        table_name = 'SchemaVersion'

class Settings(BaseModel):
    key = CharField(primary_key=True)
    value = UnknownField(null=True)  # 

    class Meta:
        table_name = 'Settings'

class Stats(BaseModel):
    action = CharField(column_name='Action', primary_key=True)
    counter = IntegerField(column_name='Counter')

    class Meta:
        table_name = 'Stats'

class Synctokens(BaseModel):
    groupid = IntegerField(column_name='groupId', constraints=[SQL("DEFAULT 0")], index=True)
    token = CharField()
    type = CharField(index=True)

    class Meta:
        table_name = 'SyncTokens'
        indexes = (
            (('groupid', 'type'), True),
        )
        primary_key = CompositeKey('groupid', 'type')

class Zoterolastsync(BaseModel):
    time = IntegerField()

    class Meta:
        table_name = 'ZoteroLastSync'
        primary_key = False

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

