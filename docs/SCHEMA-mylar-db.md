# Schema of mylar.db
## command to extract full list of tables
- $ sqlite3 mylar.db 
```bash
SQLite version 3.45.1 2024-01-30 16:01:20
Enter ".help" for usage hints.
sqlite> 

```
- sqlite> .schema --indent

CREATE TABLE storyarcs(
  StoryArcID           TEXT,
  ComicName            TEXT,
  IssueNumber          TEXT,
  SeriesYear           TEXT,
  IssueYEAR            TEXT,
  StoryArc             TEXT,
  TotalIssues          TEXT,
  Status               TEXT,
  inCacheDir           TEXT,
  Location             TEXT,
  IssueArcID           TEXT,
  ReadingOrder         INT,
  IssueID              TEXT,
  ComicID              TEXT,
  ReleaseDate          TEXT,
  IssueDate            TEXT,
  Publisher            TEXT,
  IssuePublisher       TEXT,
  IssueName            TEXT,
  CV_ArcID             TEXT,
  Int_IssueNumber      INT,
  DynamicComicName     TEXT,
  Volume               TEXT,
  Manual               TEXT,
  DateAdded            TEXT,
  DigitalDate          TEXT,
  Type                 TEXT,
  Aliases              TEXT,
  ArcImage             TEXT,
  StoreDate            TEXT
);
---------------------------------------
CREATE TABLE comics(
  ComicID              TEXT UNIQUE,
  ComicName            TEXT,
  ComicSortName        TEXT,
  ComicYear            TEXT,
  DateAdded            TEXT,
  Status               TEXT,
  IncludeExtras        INTEGER,
  Have                 INTEGER,
  Total                INTEGER,
  ComicImage           TEXT,
  FirstImageSize       INTEGER,
  ComicPublisher       TEXT,
  PublisherImprint     TEXT,
  ComicLocation        TEXT,
  ComicPublished       TEXT,
  NewPublish           TEXT,
  LatestIssue          TEXT,
  intLatestIssue       INT,
  LatestDate           TEXT,
  Description          TEXT,
  DescriptionEdit      TEXT,
  QUALalt_vers         TEXT,
  QUALtype             TEXT,
  QUALscanner          TEXT,
  QUALquality          TEXT,
  LastUpdated          TEXT,
  AlternateSearch      TEXT,
  UseFuzzy             TEXT,
  ComicVersion         TEXT,
  SortOrder            INTEGER,
  DetailURL            TEXT,
  ForceContinuing      INTEGER,
  ComicName_Filesafe   TEXT,
  AlternateFileName    TEXT,
  ComicImageURL        TEXT,
  ComicImageALTURL     TEXT,
  DynamicComicName     TEXT,
  AllowPacks           TEXT,
  Type                 TEXT,
  Corrected_SeriesYear TEXT,
  Corrected_Type       TEXT,
  TorrentID_32P        TEXT,
  LatestIssueID        TEXT,
  Collects             CLOB,
  IgnoreType           INTEGER,
  AgeRating            TEXT,
  FilesUpdated         TEXT,
  seriesjsonPresent    INT,
  dirlocked            INTEGER,
  cv_removed           INTEGER,
  not_updated_db       TEXT
);
---------------------------------------
CREATE TABLE issues(
  IssueID              TEXT,
  ComicName            TEXT,
  IssueName            TEXT,
  Issue_Number         TEXT,
  DateAdded            TEXT,
  Status               TEXT,
  Type                 TEXT,
  ComicID              TEXT,
  ArtworkURL           Text,
  ReleaseDate          TEXT,
  Location             TEXT,
  IssueDate            TEXT,
  DigitalDate          TEXT,
  Int_IssueNumber      INT,
  ComicSize            TEXT,
  AltIssueNumber       TEXT,
  IssueDate_Edit       TEXT,
  ImageURL             TEXT,
  ImageURL_ALT         TEXT,
  forced_file          INT,
  inCacheDIR           TEXT
);
---------------------------------------
CREATE TABLE snatched(
  IssueID              TEXT,
  ComicName            TEXT,
  Issue_Number         TEXT,
  Size                 INTEGER,
  DateAdded            TEXT,
  Status               TEXT,
  FolderName           TEXT,
  ComicID              TEXT,
  Provider             TEXT,
  Hash                 TEXT,
  crc                  TEXT
);
---------------------------------------
CREATE TABLE upcoming(
  ComicName            TEXT,
  IssueNumber          TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  IssueDate            TEXT,
  Status               TEXT,
  DisplayComicName     TEXT
);
---------------------------------------
CREATE TABLE nzblog(
  IssueID              TEXT,
  NZBName              TEXT,
  SARC                 TEXT,
  PROVIDER             TEXT,
  ID                   TEXT,
  AltNZBName           TEXT,
  OneOff               TEXT
);
---------------------------------------
CREATE TABLE weekly(
  SHIPDATE             TEXT,
  PUBLISHER            TEXT,
  ISSUE                TEXT,
  COMIC                VARCHAR(150),
  EXTRA                TEXT,
  STATUS               TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  CV_Last_Update       TEXT,
  DynamicName          TEXT,
  weeknumber           TEXT,
  year                 TEXT,
  volume               TEXT,
  seriesyear           TEXT,
  annuallink           TEXT,
  format               TEXT,
  rowid                INTEGER PRIMARY KEY
);
---------------------------------------
CREATE TABLE importresults(
  impID                TEXT,
  ComicName            TEXT,
  ComicYear            TEXT,
  Status               TEXT,
  ImportDate           TEXT,
  ComicFilename        TEXT,
  ComicLocation        TEXT,
  WatchMatch           TEXT,
  DisplayName          TEXT,
  SRID                 TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  Volume               TEXT,
  IssueNumber          TEXT,
  DynamicName          TEXT,
  IssueCount           TEXT,
  implog               TEXT
);
---------------------------------------
CREATE TABLE readlist(
  IssueID              TEXT,
  ComicName            TEXT,
  Issue_Number         TEXT,
  Status               TEXT,
  DateAdded            TEXT,
  Location             TEXT,
  inCacheDir           TEXT,
  SeriesYear           TEXT,
  ComicID              TEXT,
  StatusChange         TEXT,
  IssueDate            TEXT
);
---------------------------------------
CREATE TABLE annuals(
  IssueID              TEXT,
  Issue_Number         TEXT,
  IssueName            TEXT,
  IssueDate            TEXT,
  Status               TEXT,
  ComicID              TEXT,
  GCDComicID           TEXT,
  Location             TEXT,
  ComicSize            TEXT,
  Int_IssueNumber      INT,
  ComicName            TEXT,
  ReleaseDate          TEXT,
  DigitalDate          TEXT,
  ReleaseComicID       TEXT,
  ReleaseComicName     TEXT,
  IssueDate_Edit       TEXT,
  DateAdded            TEXT,
  Deleted              INT DEFAULT 0
);
---------------------------------------
CREATE TABLE rssdb(
  Title                TEXT UNIQUE,
  Link                 TEXT,
  Pubdate              TEXT,
  Site                 TEXT,
  Size                 TEXT,
  Issue_Number         TEXT,
  ComicName            TEXT
);
---------------------------------------
CREATE TABLE futureupcoming(
  ComicName            TEXT,
  IssueNumber          TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  IssueDate            TEXT,
  Publisher            TEXT,
  Status               TEXT,
  DisplayComicName     TEXT,
  weeknumber           TEXT,
  year                 TEXT
);
---------------------------------------
CREATE TABLE failed(
  ID                   TEXT,
  Status               TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  Provider             TEXT,
  ComicName            TEXT,
  Issue_Number         TEXT,
  NZBName              TEXT,
  DateFailed           TEXT
);
---------------------------------------
CREATE TABLE searchresults(
  SRID                 TEXT,
  results              Numeric,
  Series               TEXT,
  publisher            TEXT,
  haveit               TEXT,
  name                 TEXT,
  deck                 TEXT,
  url                  TEXT,
  description          TEXT,
  comicid              TEXT,
  comicimage           TEXT,
  issues               TEXT,
  comicyear            TEXT,
  ogcname              TEXT,
  sresults             TEXT
);
---------------------------------------
CREATE TABLE ref32p(
  ComicID              TEXT UNIQUE, 
  ID                   TEXT, 
  Series               TEXT, 
  Updated              TEXT
);
---------------------------------------
CREATE TABLE oneoffhistory(
  ComicName            TEXT,
  IssueNumber          TEXT,
  ComicID              TEXT,
  IssueID              TEXT,
  Status               TEXT,
  weeknumber           TEXT,
  year                 TEXT
);
---------------------------------------
CREATE TABLE jobhistory(
  JobName                TEXT,
  prev_run_datetime      timestamp,
  prev_run_timestamp     REAL,
  next_run_datetime      timestamp,
  next_run_timestamp     REAL,
  last_run_completed     TEXT,
  successful_completions TEXT,
  failed_completions     TEXT,
  status                 TEXT,
  last_date              timestamp
);
---------------------------------------
CREATE TABLE manualresults(
  provider             TEXT,
  id                   TEXT,
  kind                 TEXT,
  comicname            TEXT,
  volume               TEXT,
  oneoff               TEXT,
  fullprov             TEXT,
  issuenumber          TEXT,
  modcomicname         TEXT,
  name                 TEXT,
  link                 TEXT,
  size                 TEXT,
  pack_numbers         TEXT,
  pack_issuelist       TEXT,
  comicyear            TEXT,
  issuedate            TEXT,
  tmpprov              TEXT,
  pack                 TEXT,
  issueid              TEXT,
  comicid              TEXT,
  sarc                 TEXT,
  issuearcid           TEXT
);
---------------------------------------
CREATE TABLE ddl_info(
  ID                   TEXT UNIQUE,
  series               TEXT,
  year                 TEXT,
  filename             TEXT,
  size                 TEXT,
  issueid              TEXT,
  comicid              TEXT,
  link                 TEXT,
  status               TEXT,
  remote_filesize      TEXT,
  updated_date         TEXT,
  mainlink             TEXT,
  issues               TEXT,
  site                 TEXT,
  submit_date          TEXT,
  pack                 INTEGER,
  link_type            TEXT,
  tmp_filename         TEXT
);
---------------------------------------
CREATE TABLE exceptions_log(
  date                 TEXT UNIQUE,
  comicname            TEXT,
  issuenumber          TEXT,
  seriesyear           TEXT,
  issueid              TEXT,
  comicid              TEXT,
  booktype             TEXT,
  searchmode           TEXT,
  error                TEXT,
  error_text           TEXT,
  filename             TEXT,
  line_num             TEXT,
  func_name            TEXT,
  traceback            TEXT
);
---------------------------------------
CREATE TABLE tmp_searches(
  query_id             INTEGER,
  comicid              INTEGER,
  comicname            TEXT,
  publisher            TEXT,
  publisherimprint     TEXT,
  comicyear            TEXT,
  issues               TEXT,
  volume               TEXT,
  deck                 TEXT,
  url                  TEXT,
  type                 TEXT,
  cvarcid              TEXT,
  arclist              TEXT,
  description          TEXT,
  haveit               TEXT,
  mode                 TEXT,
  searchtype           TEXT,
  comicimage           TEXT,
  thumbimage           TEXT,
  PRIMARY KEY(query_id, comicid)
);
---------------------------------------
CREATE TABLE notifs(
  session_id           INT,
  date                 TEXT,
  event                TEXT,
  comicid              TEXT,
  comicname            TEXT,
  issuenumber          TEXT,
  seriesyear           TEXT,
  status               TEXT,
  message              TEXT,
  PRIMARY KEY(session_id, date)
);
---------------------------------------
CREATE TABLE provider_searches(
  id                   INTEGER UNIQUE,
  provider             TEXT UNIQUE,
  type                 TEXT,
  lastrun              INTEGER,
  active               TEXT,
  hits                 INTEGER DEFAULT 0
);
---------------------------------------
CREATE TABLE mylar_info(
  DatabaseVersion      INTEGER PRIMARY KEY
);
---------------------------------------
=======================================
---------------------------------------
CREATE INDEX issues_id on issues(IssueID);
---------------------------------------
CREATE INDEX comics_id on comics(ComicID);
---------------------------------------
sqlite> 
---------------------------------------
=======================================
---------------------------------------
# schema of .mylar_maintenance.db
---------------------------------------
sqlite> .schema --indent
---------------------------------------
=======================================
---------------------------------------
CREATE TABLE update_db(
  version              INT,
  mode                 TEXT PRIMARY KEY,
  status               TEXT,
  total                INT,
  current              INT,
  last_run             TEXT
);
---------------------------------------
=======================================
---------------------------------------
sqlite> 
---------------------------------------
=======================================
---------------------------------------


