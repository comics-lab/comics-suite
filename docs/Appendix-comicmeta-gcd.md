# Appendix — comicmeta-gcd

**Date:** 2025-10-21  
**Source:** [Grand Comics Database (GCD)](https://www.comics.org/download/)  
**Purpose:** Import the official GCD public data dump for local querying and normalization.

---

## Datasources

- **Primary Source:** Grand Comics Database (GCD) Public Dump  
  - Updated weekly/monthly  
  - Available as `.sql` and `.csv` archives
- **License:** Creative Commons Attribution 3.0 Unported (CC-BY 3.0)

---

## Datastores / Schema Overview

The dump includes a rich relational schema with over 20 tables. The most relevant are summarized below:

| Table | Description | Key Fields | Notes |
|--------|--------------|-------------|-------|
| `publisher` | Publisher info | `id`, `name`, `year_began` | Top-level entity |
| `series` | Comic series data | `id`, `name`, `year_began`, `publisher_id` | Maps to `Series` |
| `issue` | Individual issues | `id`, `number`, `publication_date`, `series_id` | Maps to `Issue` |
| `story` | Story-level details | `id`, `feature`, `title`, `issue_id`, `sequence_number` | Sub-record of issue |
| `creator` | Contributors | `id`, `name`, `role` | Link table for issue/story |
| `feature_type` | Story classification | `id`, `name` | e.g., "cover", "interior story" |

---

## Example Table Structure — `series`

```sql
CREATE TABLE series (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    year_began INTEGER,
    publisher_id INTEGER,
    country TEXT,
    language TEXT,
    notes TEXT
);
```

---

## Mapping to `comicbook-core` Models

| GCD Table.Field | Mapped Model | Field | Notes |
|-----------------|--------------|--------|-------|
| `series.id` | Series | `id` | |
| `series.name` | Series | `title` | |
| `series.year_began` | Series | `year` | |
| `issue.id` | Issue | `id` | |
| `issue.number` | Issue | `number` | |
| `issue.publication_date` | Issue | `date` | |

---

## Notes & Next Steps

- Implement loader that reads CSV dump → normalized SQLite schema.  
- Add incremental update mode.  
- Verify GCD license compliance (CC-BY 3.0).  
- Optional: Link to Metron/ComicVine IDs via title + year matching.
