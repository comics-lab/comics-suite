# comics-lab Documentation Guide

This directory contains centralized documentation and an index of local conversation logs for the comics-lab organization. A symlink at the workspace root (`../docs → comics-suite/docs`) provides easy access.

## Structure

- `DOCUMENTATION_INDEX.md` - Central index of all conversation logs and bookmarks (links to local repo files)
- `conversations/` - Legacy copies and historical snapshots (new logs stay local)
- `NEXT_STEPS.md` - Actionable todo items and priorities
- Other documentation (architecture, standards, etc.)

## Conversation/Transcript Policy (Local-Only)

### Adding New Transcripts

1. Create the conversation file in your package first (e.g., `your-package/CONVERSATION.md`)
2. Keep bookmarks and action logs in your package (e.g., `BOOKMARKS.md`, `Action-Log.md`)
3. Update `DOCUMENTATION_INDEX.md` to list the local files with a short summary
4. Add a pointer in your package README.md to the local log files

### Storage Policy

We use a local-only approach:
- Keep all logs in the repo where the work happened
- Do not copy logs into org-wide folders
- Use `DOCUMENTATION_INDEX.md` for discoverability only

### Naming Conventions

- Conversations: `your-package/CONVERSATION.md`
- Bookmarks: `your-package/BOOKMARKS.md`
- Action logs: `your-package/Action-Log.md`

### Who Can Add Transcripts

- Package maintainers should preserve significant development conversations
- Focus on architectural decisions, major refactors, and integration notes
- Include test results and verification steps when relevant

## Quick Start

To add a new conversation:

```bash
# 1. Create local copy in your package
touch your-package/CONVERSATION.md

# 2. Add content to your local copy
vim your-package/CONVERSATION.md

# 3. Update the index
vim docs/DOCUMENTATION_INDEX.md

# 4. Add pointers in your README
echo "See: CONVERSATION.md, BOOKMARKS.md, Action-Log.md" >> your-package/README.md
```

## Maintenance

- Review `DOCUMENTATION_INDEX.md` periodically to ensure all links work
- Archive old conversations by moving them to `archive/` within the repo where they originated
- Keep `NEXT_STEPS.md` updated as items are completed
