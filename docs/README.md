# comics-lab Documentation Guide

This directory contains centralized documentation, conversation logs, and project artifacts for the comics-lab organization. A symlink at the workspace root (`../docs → comics-suite/docs`) provides easy access.

## Structure

- `DOCUMENTATION_INDEX.md` - Central index of all conversation logs and bookmarks
- `conversations/` - Full transcripts and logs
- `NEXT_STEPS.md` - Actionable todo items and priorities
- Other documentation (architecture, standards, etc.)

## Conversation/Transcript Policy

### Adding New Transcripts

1. Create the conversation file in your package first (e.g., `your-package/CONVERSATION.md`)
2. Add a copy to `docs/conversations/your-package_FULL_CONVERSATION.md`
3. Update `DOCUMENTATION_INDEX.md` to list both locations
4. Add a pointer in your package README.md to `../docs/DOCUMENTATION_INDEX.md`

### Copy vs Move Policy

We use a "copy-and-link" approach:
- Keep the original conversation file in its package
- Create a full copy in `docs/conversations/`
- Add pointers in package READMEs to the central docs
- This preserves local package history while enabling central discovery

### Naming Conventions

- Package conversations: `your-package/CONVERSATION.md`
- Central copies: `docs/conversations/your-package_FULL_CONVERSATION.md`
- Bookmarks: `docs/conversations/your-package_BOOKMARKS.md`
- Action logs: `docs/conversations/your-package_Action-Log.md`

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

# 3. Create central copy
cp your-package/CONVERSATION.md docs/conversations/your-package_FULL_CONVERSATION.md

# 4. Update the index
vim docs/DOCUMENTATION_INDEX.md

# 5. Add pointer in your README
echo "See: ../docs/DOCUMENTATION_INDEX.md" >> your-package/README.md
```

## Maintenance

- Review `DOCUMENTATION_INDEX.md` periodically to ensure all links work
- Archive old conversations by moving them to `conversations/archive/` when superseded
- Keep `NEXT_STEPS.md` updated as items are completed