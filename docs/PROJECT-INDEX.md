# Comics-Lab Project Index

**Date:** 2025-10-21  
**Organization:** comics-lab (GitHub)  
**License:** MIT  
**Language:** Python 3 only  

## Overview

The **comics-lab** organization is a suite of coordinated Python 3 utilities and connectors designed to manage and enrich comic book collections. It follows a **multi-repository architecture** with each repository focused on one responsibility while sharing a common core library.

## Repository Structure

### Core Library
- **comicbook-core** - Shared library providing common models, naming logic, CSV reporting, and logging utilities
  - Location: `./comicbook-core/`
  - Status: Repository skeleton with placeholder implementations
  - Dependencies: None (core library)

### Application Tools
- **mylar3-sanity** - SQLite + filesystem sanity checker for Mylar3
  - Location: `./mylar3-sanity/`
  - Dependencies: `rarfile>=4.2`, comicbook-core
  - Purpose: Verifies DB integrity, file presence, naming consistency

- **cbz-doctor** - CBZ validator and repair tool
  - Location: `./cbz-doctor/`
  - Dependencies: `rarfile>=4.2`
  - Purpose: Validates archives, repairs ComicInfo.xml, emits Metron XML

- **comic-file-organizer** - Directory scanner, renamer, and importer
  - Location: `./comic-file-organizer/`
  - Dependencies: `rarfile>=4.2`
  - Purpose: Converts CBR→CBZ, renames per Mylar rules, updates Mylar3

### Metadata Connectors
- **comicmeta-comicvine** - ComicVine API connector
  - Location: `./comicmeta-comicvine/`
  - Dependencies: `requests>=2.31.0`
  - Purpose: Fetches and normalizes metadata from ComicVine

- **comicmeta-metron** - Metron/Mokkari API connector
  - Location: `./comicmeta-metron/`
  - Dependencies: None specified
  - Purpose: Import/export XML metadata via Metron APIs

- **comicmeta-gcd** - Grand Comics Database loader
  - Location: `./comicmeta-gcd/`
  - Dependencies: None specified
  - Purpose: Parses GCD dump files, normalizes to shared models

### Meta/Documentation
- **comics-suite** - Meta-repository for documentation and coordination
  - Location: `./comics-suite/`
  - Purpose: Central documentation, automation scripts, project governance
  - Contains: docs/, scripts/, GitHub automation tools

- **.github** - Organization-level GitHub configuration
  - Location: `./.github/`
  - Contains: Organization profile, project setup guides, security documentation

## Technical Architecture

### Common Features (All Repositories)
- Unified CLI pattern: `--dry-run`, `--apply`, `--log-file`, `--report`
- Rotating log files (5MB × 3 backups)
- CSV reporting with 1-based line numbering
- MIT License
- Python 3 only
- Standard Makefile targets: `venv`, `test`, `clean`

### Data Models (in comicbook-core)
- **Series**: id, title, year, publisher, volume, aliases
- **Issue**: id, series_id, number, year, date, title, variant, barcode
- **FileRecord**: path, size, extension, series_hint, issue_hint
- **ComicInfo**: series, number, year, title, volume, publisher, web, notes, tags

### Development Standards
- **Branching Strategy**: `main` (protected), `feature/*`, `release/*`
- **CI/CD**: GitHub Actions with build/test + CodeQL + Secret scanning
- **Security**: 2FA required, secret scanning enabled, PR reviews required
- **Dependencies**: Minimal external dependencies, Python standard library preferred

## Repository Status

| Repository | Status | Implementation | Git Status |
|------------|--------|----------------|------------|
| comicbook-core | Skeleton | Placeholder models/config | Individual git repo |
| mylar3-sanity | Skeleton | CLI stub | Individual git repo |
| cbz-doctor | Skeleton | CLI stub | Individual git repo |
| comic-file-organizer | Skeleton | CLI stub | Individual git repo |
| comicmeta-comicvine | Skeleton | CLI stub | Individual git repo |
| comicmeta-metron | Skeleton | CLI stub | Individual git repo |
| comicmeta-gcd | Skeleton | CLI stub | Individual git repo |
| comics-suite | Documentation | Complete docs + scripts | Individual git repo |
| .github | Configuration | Organization profile + guides | Individual git repo |

## File Structure Overview

```
comics-lab/
├── cbz-doctor/                 # CBZ validator and repair tool
│   ├── cbz_doctor/
│   │   ├── __init__.py
│   │   └── cli.py
│   ├── LICENSE (MIT)
│   ├── Makefile
│   ├── README.md
│   └── requirements.txt
├── comicbook-core/            # Shared core library
│   ├── comicbook_core/
│   │   ├── __init__.py
│   │   ├── config_naming.py
│   │   ├── logging_utils.py
│   │   ├── models.py
│   │   └── report.py
│   ├── LICENSE (MIT)
│   ├── Makefile
│   ├── README.md
│   └── requirements.txt
├── comic-file-organizer/      # File scanner and organizer
│   ├── comic_file_organizer/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── [standard files]
├── comicmeta-comicvine/       # ComicVine API connector
│   ├── comicmeta_comicvine/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── [standard files]
├── comicmeta-gcd/             # GCD dump loader
│   ├── comicmeta_gcd/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── [standard files]
├── comicmeta-metron/          # Metron API connector
│   ├── comicmeta_metron/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── [standard files]
├── comics-suite/              # Meta-repository
│   ├── archive/
│   ├── docs/
│   │   ├── Action-Log.md
│   │   ├── Architecture.md
│   │   ├── Repo-Standards.md
│   │   └── Security-Checklist.md
│   ├── scripts/
│   │   ├── apply_all.sh
│   │   ├── enable_security.sh
│   │   ├── lockdown_actions.sh
│   │   ├── protect_branches.sh
│   │   ├── seed_repos.sh
│   │   ├── setup_org.sh
│   │   └── verify.sh
│   ├── LICENSE (MIT)
│   └── README.md
├── .github/                   # Organization configuration
│   ├── profile/
│   │   └── README.md
│   ├── LICENSE (MIT)
│   └── Project-Setup-Guide.md
└── mylar3-sanity/            # Mylar3 database checker
    ├── mylar3_sanity/
    │   ├── __init__.py
    │   └── cli.py
    └── [standard files]
```

## Implementation Roadmap

| Milestone | Description | Status |
|-----------|-------------|--------|
| **M0** | Project skeleton and organization setup | ✅ Complete |
| **M1** | Refactor mylar3-sanity to use comicbook-core | 🟡 Pending |
| **M2** | Finalize ComicVine + GCD connectors; develop Metron MVP | 🟡 Pending |
| **M3** | Build cbz-doctor validator and repair workflow | 🟡 Pending |
| **M4** | Implement comic-file-organizer for renaming and DB sync | 🟡 Pending |
| **M5** | Full integration testing and documentation | 🟡 Pending |

## Example Usage Commands

```bash
# mylar3-sanity
mylar3-sanity --db mylar.db --library /mnt/comics --config config.ini --report sanity.csv

# comicmeta-comicvine
comicvine --query "Spider-Man" --out series.csv --cache .cache

# cbz-doctor
cbz-doctor scan --root /comics --fix-comicinfo --write-metron-xml --dry-run

# comic-file-organizer
organizer import --root /incoming --library /comics --config config.ini --convert-cbr --apply
```

## Security & Governance

- **Organization**: comics-lab on GitHub
- **Teams**: owners, maintainers, contributors, readers
- **Security**: 2FA required, secret scanning enabled, CodeQL analysis
- **Branch Protection**: All merges to `main` require PR approval
- **Access Control**: Private repos by default, public when stable

## Dependencies Summary

| Package | Used By | Version | Purpose |
|---------|---------|---------|---------|
| rarfile | cbz-doctor, comic-file-organizer, mylar3-sanity | >=4.2 | RAR archive handling |
| requests | comicmeta-comicvine | >=2.31.0 | HTTP API calls |

## Action Log

- **2025-10-20** — Initial project skeleton created with all repositories
- **2025-10-19** — Repository structure defined and documented
- **2025-10-21** — Project indexing completed for organization-level deployment

---

*This index provides comprehensive documentation for the comics-lab organization project structure, suitable for GitHub organization-level deployment and team coordination.*