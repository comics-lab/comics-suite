# Appendix — comicmeta-metron

**Date:** 2025-10-21  
**Source:** [Metron Project](https://github.com/Metron-Project/mokkari) and [Metron Tagger](https://github.com/Metron-Project/metron-tagger)  
**Purpose:** Integrate Metron/Mokkari metadata XML files into the shared model and support cross-tagging between Mylar3, GCD, and ComicVine.

---

## Datasources

- **Primary Source:** Mokkari (Metron Cloud API)  
  Provides structured XML for comic metadata, used by Metron Tagger.
- **Secondary Source:** Local XML files created by Metron Tagger  
  Used for tagging and identification of CBZ files.

---

## Datastores / Schema Overview

The primary datastore is **XML-based**, organized as one file per series or issue.  
Common elements include:

| Element | Description | Example |
|----------|--------------|----------|
| `<Series>` | Container for all issues of a title | Attributes: `title`, `publisher`, `volume`, `year` |
| `<Issue>` | Single comic issue | Attributes: `number`, `date`, `title` |
| `<Credit>` | Creator or contributor entry | Attributes: `name`, `role` |
| `<Tag>` | Metadata tag | Attributes: `type`, `value` |
| `<File>` | File association | Attributes: `path`, `checksum` |

---

## Example XML Structure

```xml
<Series title="The Amazing Spider-Man" publisher="Marvel" volume="1" year="1963">
  <Issue number="1" date="1963-03-01" title="Spider-Man!">
    <Credit name="Stan Lee" role="Writer"/>
    <Credit name="Steve Ditko" role="Artist"/>
    <Tag type="Genre" value="Superhero"/>
    <File path="/comics/Marvel/Spider-Man 001.cbz" checksum="abcd1234"/>
  </Issue>
</Series>
```

---

## Mapping to `comicbook-core` Models

| Metron Element | Mapped Model | Field | Notes |
|----------------|--------------|--------|-------|
| `Series.@title` | Series | `title` | |
| `Series.@year` | Series | `year` | |
| `Issue.@number` | Issue | `number` | |
| `Issue.@date` | Issue | `date` | |
| `Issue.@title` | Issue | `title` | |
| `Credit.@name` | Person | `name` | |
| `Credit.@role` | Person | `role` | |

---

## Notes & Next Steps

- Develop parser for Metron XML → `comicbook-core` models.  
- Validate schema compatibility with Mylar3 and ComicVine.  
- Determine best practices for merging credit and tag data between connectors.
