# Appendix — comicmeta-comicvine

**Date:** 2025-10-21  
**Source:** [ComicVine API](https://comicvine.gamespot.com/api/)  
**Purpose:** Provide normalized metadata from the ComicVine REST API into `comicbook-core` shared models.

---

## Datasources

- **Primary Source:** ComicVine REST API (Gamespot / Fandom)  
  Base URL: `https://comicvine.gamespot.com/api/`
- **Response Format:** JSON envelope with pagination and metadata.
- **Access:** Requires API key (`api_key`) and `format=json`.

---

## Datastores / Schema Overview

ComicVine exposes multiple **resources**, each analogous to a table:

| Resource | Description | Key Fields | Notes |
|-----------|--------------|-------------|-------|
| `volume` | Represents a comic series. | `id`, `name`, `publisher`, `start_year`, `count_of_issues` | Maps to `Series` model |
| `issue` | Represents a single issue in a volume. | `id`, `name`, `issue_number`, `cover_date`, `store_date`, `volume` | Maps to `Issue` model |
| `character` | Characters appearing in issues. | `id`, `name`, `real_name`, `publisher` | Optional metadata |
| `publisher` | Comic publishers. | `id`, `name`, `deck` | Used for normalization |
| `story_arc` | Multi-issue arcs or crossovers. | `id`, `name`, `deck` | Optional linking table |
| `person` | Creators and contributors. | `id`, `name`, `site_detail_url` | Used in relationships |
| `team` | Teams appearing in comics. | `id`, `name`, `deck` | Optional |

---

## Example Resource Schema (Volume)

```json
{
  "error": "OK",
  "limit": 100,
  "offset": 0,
  "number_of_page_results": 100,
  "number_of_total_results": 40000,
  "status_code": 1,
  "results": [
    {
      "id": 260,
      "name": "The Amazing Spider-Man",
      "publisher": { "id": 31, "name": "Marvel" },
      "start_year": "1963",
      "count_of_issues": 441,
      "site_detail_url": "https://comicvine.gamespot.com/the-amazing-spider-man/4050-260/"
    }
  ]
}
```

---

## Mapping to `comicbook-core` Models

| ComicVine Field | Mapped Model | Field | Notes |
|-----------------|--------------|--------|-------|
| `volume.id` | Series | `id` | Primary key |
| `volume.name` | Series | `title` | Series name |
| `volume.start_year` | Series | `year` | Year of first issue |
| `issue.id` | Issue | `id` | Issue ID |
| `issue.issue_number` | Issue | `number` | Issue number |
| `issue.cover_date` | Issue | `date` | Publication date |
| `issue.name` | Issue | `title` | Issue title |

---

## Notes & Next Steps

- Add pagination + caching to limit API rate usage (1 request/sec).  
- Review licensing: ComicVine data use permitted for personal/non-commercial projects.  
- Future task: Mirror selected metadata locally into a normalized SQLite datastore.
