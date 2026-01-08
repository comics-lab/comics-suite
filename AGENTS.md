# AGENTS.md — ORG\_\_comics_lab

- file created 01/08/2026

## Purpose

This file defines the **operational contract** for AI-assisted agents (ChatGPT, Codex, Copilot, CLI agents, etc.) working within the **ORG\_\_comics_lab** ecosystem.

Its goals are to:

- Establish a **shared mental model** across browser-based ChatGPT Projects and IDE-based agents (VS Code Codex/Copilot).
- Encode architectural intent, boundaries, and priorities.
- Prevent context loss between conversational reasoning and task-oriented code execution.
- Act as a durable, version-controlled bridge between **thinking** and **doing**.

This file is authoritative.

---

## Scope

ORG\_\_comics_lab spans **two tightly coupled domains**:

1. **Multi-repository software ecosystem** for comic library management
2. **Home lab infrastructure & operations documentation** that runs and sustains that software

Agents must treat **code, data, and infrastructure** as a single system.

---

## Canonical Repositories (GitHub Organization: `comics-lab`)

Agents should assume a multi-repo workspace containing, at minimum:

### Core & Shared Logic

- `comicbook-core` — canonical models, naming rules, shared utilities

### Metadata & Ingest Pipelines

- `comicmeta-comicvine`
- `comicmeta-metron`
- `comicmeta-gcd`

### Validation / Repair / Tooling

- `cbz-doctor`
- `mylar3-sanity`
- `comic-file-organizer`
- `comictagger`

### Application Layer

- `mylar3`
- `mylar3-test` (experimental / integration work)

### Coordination & Governance

- `comics-suite` — documentation index, standards, meta-structure
- `.github` — org-level workflows, policies
- `org_level_Scripts` — operational scripts

Agents must **not** introduce new repos without justification.

---

## Documentation Domain (Home Lab + Operations)

In addition to software, this Project includes **first-class documentation** for:

- Home lab server design
- Storage architecture (NVMe, RAID, Btrfs, backups)
- Deployment of the comics-lab software stack
- Maintenance, monitoring, and recovery

This documentation is not ancillary — it is part of the system.

Agents must:

- Treat docs as production artifacts
- Keep docs in sync with code behavior
- Prefer Markdown under `docs/`

---

## Source of Truth Hierarchy

Agents must resolve ambiguity using the following precedence:

1. **This AGENTS.md file**
2. `docs/DOCUMENTATION_INDEX.md`
3. Repo-level `README.md`
4. Code comments and tests
5. Conversational context (ChatGPT threads)

When conflicts exist, escalate rather than guessing.

---

## Operating Principles

### 1. Separation of Concerns (Real Simplifier Doctrine)

- **Server** = API / orchestration / I/O
- **Services** = pure, testable business logic

Agents should:

- Prefer extracting logic into service modules
- Avoid embedding long-running or blocking work in web servers
- Prepare code for job-queue execution (RQ/Redis-style)

### 2. Minimal Change, Maximum Clarity

- Small, reviewable changes
- Reversible commits
- Avoid cleverness that obscures intent

### 3. Shared Models First

If logic or structure could live in `comicbook-core`, it probably should.
Duplication across repos is a smell.

---

## Agent Behavior Expectations

### Before Acting

Agents must:

1. Read this file
2. Read `docs/DOCUMENTATION_INDEX.md`
3. Identify which repo(s) are authoritative for the task

### While Acting

Agents must:

- Respect existing patterns
- Preserve backward compatibility unless explicitly told otherwise
- Update docs when behavior changes

### After Acting

Agents should:

- Summarize changes
- Note assumptions
- Flag follow-up work

---

## ChatGPT ↔ IDE Agent Bridge

Because browser-based ChatGPT and IDE-based agents do not share live memory:

- **Docs are the bridge**
- Decisions must be written down
- State must be externalized

Agents should prefer:

- `docs/PROJECT_CONTEXT.md`
- `docs/DECISIONS.md`
- `docs/NEXT_STEPS.md`

If information matters tomorrow, it belongs in docs.

---

## Allowed Autonomy

Agents MAY:

- Read across repos
- Propose refactors
- Generate documentation
- Suggest architectural changes

Agents MUST NOT:

- Perform destructive operations without confirmation
- Rewrite history casually
- Introduce new infra dependencies without discussion

---

## Tone & Style

- Technical, calm, precise
- No unnecessary verbosity in code
- Documentation should be clear, instructional, and durable

Humor is allowed in conversation — not in production code.

---

## When in Doubt

Stop.
Document the uncertainty.
Ask.

Silence is worse than a question.

---

## Axiom

> The code is important.
> The data is sacred.
> The documentation is the memory.

Agents exist to protect all three.
