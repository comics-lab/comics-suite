# Knowledge Files and Documentation Index Guide

This guide explains where to place "truth files," how to log conversations,
and how to keep a shared documentation index without centralizing the logs.

## Repo Type Placement (Quick Matrix)

Use this as default placement guidance:

- Suite repo: templates, playbooks, shared non-sensitive skills, docs index.
- Team core repo: local truth files, local logs, team-specific skills and docs.
- Collab repo: shared specs, joint decisions, shared glossary (opt-in only).

If a file does not belong in a collab repo, keep it in the team repo and copy
only the minimal shared excerpt with attribution.

## Truth Files

### AGENTS.md
Use when:
- Defining scope, isolation rules, tool boundaries, and allowed sources.
- Referencing the org-level master profile when applicable.
Update when:
- Scope or access rules change.

### COMPREHENSION.md
Use when:
- Capturing the current system understanding and data flow.
- Recording assumptions or constraints.
Update when:
- New insights or corrections are discovered.

### DECISIONS.md
Use when:
- Making a significant choice that affects design, workflow, or policy.
Update when:
- A decision is revised or reversed.

### ROADMAP.md
Use when:
- Defining goals, milestones, and near-term steps.
Update when:
- Priorities or timelines change.

### GLOSSARY.md
Use when:
- Introducing domain terms, acronyms, or naming conventions.
Update when:
- New terms or definitions are added.

### SKILLS/
Use when:
- Capturing repeatable workflows for agents.
Update when:
- A workflow changes or is refined.

## Logging Policy (Local-Only)

Log significant decisions and transcripts so they remain discoverable and
reproducible, but keep logs in the repo where the work happened.

Required local files (when applicable):
- `CONVERSATION.md`
- `BOOKMARKS.md`
- `Action-Log.md` (or `ACTION_LOG.md`)

Do not copy or move logs into org-wide folders.

## Documentation Index (Link-Only)

Maintain a docs index (example: `docs/DOCUMENTATION_INDEX.md`) that lists
local log files, truth files, and key artifacts across repos. The index should:

- Link to the canonical local file path.
- Include a short summary of content and why it matters.
- Avoid duplicating the content itself.

## One-Way Copying With Attribution

When a team reuses collab knowledge:

- Copy the minimal necessary content into the team repo.
- Include source repo and path in a short attribution note.
- Avoid linking to external files for ongoing runtime dependency.
