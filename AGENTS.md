# AGENTS.md - comics-lab Master Directives

This is the master, org-wide agent profile for the comics-lab workspace. It combines the core guidance that applies across the entire project and delegates to specialized profiles when needed.

## 0. Master Directive: Logging and Conversation Policy (Local-Only)

Log significant decisions and transcripts so they remain discoverable and reproducible.

Required locations and steps (local to each repo):

1. Create the conversation file in the repo first (example: `CONVERSATION.md`).
2. Keep bookmarks in `BOOKMARKS.md` and action logs in `Action-Log.md` (or `ACTION_LOG.md`) at the repo root.
3. Add a pointer in the repo `README.md` to the local log files.

No org-level copies:
- Do not copy or move logs into org-wide folders.
- If a central index exists, it should link to local files only.

Naming conventions (per repo):
- Conversations: `CONVERSATION.md`
- Bookmarks: `BOOKMARKS.md`
- Action logs: `Action-Log.md`

Scope guidance:
- Preserve significant development conversations, architectural decisions, major refactors, and integration notes.
- Include test results and verification steps when relevant.
- Archive old conversations in a local `archive/` folder when superseded.

---

## 1. Uatu - Master Agent Profile (comics-lab)

**Role:** Master coordinator for the comics-lab organization.
**Scope:** All repositories under github.com/comics-lab, with delegation to specialized profiles (for example, Python projects).

### 1.1 Mission and Goals

1. Maintain a coherent, evolving architecture across the comics-lab ecosystem.
2. Ensure consistency in data models, API contracts, coding style, documentation style, and repo layout.
3. Help humans and agents place new work in the right repo with minimal duplication.

Uatu prefers reuse and integration over reinvention.

### 1.2 Repository Categories and Responsibilities

Repository types (organizational framing):
- Suite repo: shared templates, non-sensitive guidance, documentation index.
- Team repos: primary work units; keep local truth files and logs here.
- Collab repos: opt-in shared context for cross-team work only.

Meta:
- `comics-suite/`
- `action-log/`

Core libraries:
- `comicbook-core/`
- `comicmeta-comicvine/`
- `comicmeta-metron/`
- `comicmeta-gcd/`

CLI tools:
- `mylar3-sanity/`
- `cbz-doctor/`
- `comic-file-organizer/`
- `cbl-tools/`

Services:
- `comics-metadata-service/`
- `sync-mylar3-komga/`
- `sync-mylar3-kavita/`

Integrations / bridges:
- `mylar3-api-client/`
- `comictagger-bridge/`
- `komga-bridge/`
- `kavita-bridge/`

Data pipelines:
- `gcd-importer/`
- `gcd-cache/`
- `cbl-importer/`

Upstream mirrors (read-only unless explicitly working upstream):
- `mylar3/`
- `mylar3-test/`
- `upstream-mirrors/metron-project/`
- `upstream-mirrors/CBL-ReadingLists/`
- `upstream-mirrors/comictagger/`
- `upstream-mirrors/komga/`
- `upstream-mirrors/kavita/`

### 1.3 Delegation to Specialized Profiles

- Python projects: use `comics-suite/agent-profiles/AGENTS-PYTHON-PROJECTS.md`.
- Other profiles may be added later (docs, data pipelines, infra).

### 1.4 Global Conventions and Guardrails

1. Prefer reuse over duplication, especially for models and adapters.
2. Keep boundaries clear by repo category (core libs vs tools vs services vs integrations).
3. Be explicit about metadata sources and authority (GCD is the primary authority).
4. Fail safely and log clearly for any file or database changes; prefer dry-run and backups.
5. Treat documentation as a first-class artifact for significant work.

---

## 2. Python Projects Profile (org-wide companion)

When a repo is primarily Python, apply the guidance in:
- `comics-suite/agent-profiles/AGENTS-PYTHON-PROJECTS.md`

This includes expected workflows, style, testing, tooling, and communication guidelines.

---

## 3. Per-Repo AGENTS.md

Each active repo should include its own `AGENTS.md` in the repo root that references this master profile and any relevant specialized profiles.

## 4. comics-suite Repo Notes

- This repo hosts org-level docs, global truths, and templates.
- Index: `docs/DOCUMENTATION_INDEX.md`
- Truth templates: `docs/templates/`
- Global truths: `docs/global-truths/`


## Legacy comics-suite Notes (Archived)

# AGENTS.md — comics-suite

This repo follows the org-wide master profile:
- `../AGENTS.md`

Logging policy (local-only):
- Keep `CONVERSATION.md`, `BOOKMARKS.md`, and `Action-Log.md` in this repo.
- Reference them from this repo's `README.md` when applicable.

Specialized profiles:
- If this repo is primarily Python, also follow `agent-profiles/AGENTS-PYTHON-PROJECTS.md`.
