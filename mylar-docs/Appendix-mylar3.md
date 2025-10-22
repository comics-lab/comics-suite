
# Appendix — Mylar3

**Date:** 2025-10-21  
**Scope:** Estimated schema & configuration overview for planning and integration.  
**Target docs path:** `comics-lab/comics-suite/mylar-docs/`

> ⚠️ **Note:** This appendix contains an **estimated** schema and field list compiled from prior work and common Mylar3 usage patterns. We will replace with **actuals** by exporting the live SQLite DB schema and harvesting the current `config.ini` keys in a later pass.

---

## 1) Datasources

- **SQLite DB**: `mylar.db` (primary application datastore)
- **Configuration**: `config.ini` (naming rules, providers, paths, API keys)
- **Series cache**: `series.json` (per‑series local cache / hints)
- **External**: ComicVine, GCD (planned), Metron (planned)
- **Filesystem**: Library root containing `cbz` / `cbr` files

---

## 2) Datastores / Estimated Schema Overview (SQLite)

### Key Entities & Relationships
- **Series** 1—N **Issues**
- **Issues** N—M **StoryArcs**
- **Issues** 1—N **Downloads/Snatches**
- **Publishers** 1—N **Series**

### Estimated Tables

#### `series`
```sql
CREATE TABLE series (
  id              INTEGER PRIMARY KEY,   -- internal series id
  comicvine_id    INTEGER,               -- CV volume id (4050-xxxxx numeric part)
  title           TEXT NOT NULL,
  year_began      INTEGER,               -- first publication year
  publisher_id    INTEGER,               -- -> publishers.id
  volume          INTEGER,               -- series volume number if available
  status          TEXT,                  -- ongoing/ended/etc
  sort_title      TEXT,                  -- normalized title for sorting
  aliases         TEXT,                  -- comma/pipe-separated aliases
  added_on        TEXT,                  -- ISO timestamp
  last_updated    TEXT                   -- ISO timestamp
);
```

#### `issues`
```sql
CREATE TABLE issues (
  id              INTEGER PRIMARY KEY,
  series_id       INTEGER NOT NULL,      -- -> series.id
  comicvine_id    INTEGER,               -- CV issue id (4000-xxxxx numeric part)
  number          TEXT NOT NULL,         -- issue number (string to allow 1A, 0.5, etc)
  title           TEXT,
  cover_date      TEXT,                  -- yyyy-mm-dd
  store_date      TEXT,                  -- yyyy-mm-dd
  publication_year INTEGER,
  variant_of_id   INTEGER,               -- -> issues.id (parent issue for variants)
  barcode         TEXT,
  file_path       TEXT,                  -- resolved path if downloaded
  file_hash       TEXT,                  -- optional content hash
  size_bytes      INTEGER,
  downloaded      INTEGER DEFAULT 0,     -- 0/1
  archived        INTEGER DEFAULT 0,     -- archive removed from wanted list, etc.
  created_on      TEXT,
  updated_on      TEXT
);
```

#### `publishers`
```sql
CREATE TABLE publishers (
  id            INTEGER PRIMARY KEY,
  name          TEXT NOT NULL,
  country       TEXT,
  notes         TEXT
);
```

#### `storyarcs`
```sql
CREATE TABLE storyarcs (
  id            INTEGER PRIMARY KEY,
  name          TEXT NOT NULL,
  description   TEXT,
  start_year    INTEGER
);
```

#### `storyarc_issues`  (join table)
```sql
CREATE TABLE storyarc_issues (
  storyarc_id   INTEGER NOT NULL,   -- -> storyarcs.id
  issue_id      INTEGER NOT NULL,   -- -> issues.id
  sequence_num  INTEGER,            -- optional ordering within arc
  PRIMARY KEY (storyarc_id, issue_id)
);
```

#### `downloads`  (or `snatched` / `history`)
```sql
CREATE TABLE downloads (
  id            INTEGER PRIMARY KEY,
  issue_id      INTEGER NOT NULL,   -- -> issues.id
  source        TEXT,               -- sabnzbd, qbittorrent, blackhole, manual
  status        TEXT,               -- grabbed, downloaded, post-processed, failed
  added_on      TEXT,               -- ISO timestamp
  completed_on  TEXT,               -- ISO timestamp
  log           TEXT                -- json/text of processing log
);
```

> **When we extract the actual schema**, we’ll verify table names/fields and adjust accordingly (e.g., tables like `comics` vs `series`, `snatched`, `issue_status` etc.).

---

## 3) Configuration (`config.ini`) — Estimated Annotation

> We will replace this with a definitive, section‑by‑section annotation from the live `config.ini` later. Below is a curated outline to anchor integration.

### `[General]`
- `library_root`: Root path for library storage (destination of organized files)
- `download_dir`: Incoming / watch folder for new items
- `log_dir`: Directory for log files
- `cache_dir`: Temporary/cache path
- `timezone`: TZ handling for schedules

### `[WebServer]`
- `host`, `port`
- `http_root` (base path), `api_key`
- `enable_https`, `certfile`, `keyfile`

### `[Naming]`
- `series_dir_format`: e.g., `{publisher}/{series} ({seriesyear})`
- `issue_filename_format`: e.g., `{series} - {issuenumber} ({year})`
- `lowercase`, `replace_spaces`, `unicode_normalization`
- `move_on_scan`: true/false (post-processing action)

### `[ComicVine]`
- `api_key`: ComicVine token
- `rate_limit`: ms or requests/sec

### `[Providers]` / `[Downloaders]`
- Integrations for **SABnzbd**, **qBittorrent**, **NZBGet**, **Transmission** etc.
  - Host/Port/Auth fields
  - Category/Label
  - Post-processing flags

### `[PostProcessing]`
- `convert_cbr_to_cbz`: true/false
- `rename_and_move`: true/false
- `write_comicinfo_xml`: true/false
- `extract_metadata`: true/false

### `[Advanced]`
- `scan_threads`: concurrency for filesystem scanning
- `db_backup_interval`: days/hours
- `api_timeout`: seconds

---

## 4) `series.json` (Per-Series Cache) — Estimated

Typical fields (varies by build/config):
```json
{{
  "series_id": 12345,
  "title": "The Amazing Spider-Man",
  "publisher": "Marvel",
  "year_began": 1963,
  "issues_cached": 441,
  "last_sync": "2025-09-10T14:32:00Z"
}}
```

---

## 5) Mapping to `comicbook-core` Models

| Mylar3 Field | Model | Field | Notes |
|--------------|-------|-------|-------|
| `series.id` | Series | `id` | Internal numeric ID |
| `series.title` | Series | `title` | |
| `series.year_began` | Series | `year` | |
| `series.publisher_id` → `publishers.name` | Series | `publisher` | via join |
| `issues.id` | Issue | `id` | |
| `issues.series_id` | Issue | `series_id` | |
| `issues.number` | Issue | `number` | String type for variants |
| `issues.cover_date` | Issue | `date` | |
| `issues.title` | Issue | `title` | |
| `issues.barcode` | Issue | `barcode` | |

---

## 6) Extracting the Actual Schema (Planned)

### Option A: sqlite3 shell
```bash
sqlite3 /path/to/mylar.db ".schema" > schema.sql
sqlite3 /path/to/mylar.db "PRAGMA table_info(series);" > series_columns.txt
```

### Option B: Python snippet
```python
import sqlite3
con = sqlite3.connect("mylar.db")
cur = con.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name;")
for name, sql in cur:
    print(f"\n-- {name}\n{sql}")
```

We’ll replace the **estimated** DDL above with the exported actuals and annotate each field.

---

## 7) Operational Notes & Next Steps

- Add a `mylar3-connector` or enrich `mylar3-sanity` to dump/verify schema on demand.
- Confirm naming tokens used in Mylar3 match your `comicbook-core` renderers.
- Decide on canonical source for **publisher** and **storyarc** nomenclature (GCD vs CV vs Metron).
- Schedule periodic DB backups and vacuum (post heavy imports).

---

**End of Appendix — Mylar3**
