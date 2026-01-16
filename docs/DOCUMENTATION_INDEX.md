# Documentation Index — comics-lab

This index lists local conversation logs, bookmarks, and action logs across the workspace. It points to the canonical location of each artifact and contains a short summary to help with discoverability. Logs remain in their originating repos.

Files discovered and short summaries

- comic-file-organizer/CONVERSATION.md
  - Path: comic-file-organizer/CONVERSATION.md
  - Summary: Full integration conversation and decisions for the Disk-Folder-File Analyzer (DFA) vendor-copy into `comic-file-organizer`. Describes scanner changes (followlinks, inode tracking, hardlink dedupe, symlink loop avoidance), tests added, and commands used to verify behavior.

- comic-file-organizer/BOOKMARKS.md
  - Path: comic-file-organizer/BOOKMARKS.md
  - Summary: Integration bookmark for the DFA vendor-copy; includes key artifacts, locations, and test verification commands.

- comic-file-organizer/README_EXTRA.md (if present)
  - Path: comic-file-organizer/README_EXTRA.md
  - Summary: Additional README material summarizing changes and how to run tests (may be local to the integrated scanner).

- org_level_Scripts/README.md
  - Path: org_level_Scripts/README.md
  - Summary: Conversation log and diagnosis related to `git_pull.sh` and `git_push.sh`, including the root cause of a loop hang, the applied fixes (use `mapfile` + array), and usage examples.

- comics-suite/docs/Action-Log.md
  - Path: comics-suite/docs/Action-Log.md
  - Summary: Chronological action log for comics-suite meta-operations and snapshots.

Legacy copies in `docs/conversations/` (pre-local-only policy):

- `docs/conversations/comic-file-organizer_FULL_CONVERSATION.md` — full conversation transcript (copy of `comic-file-organizer/CONVERSATION.md`).
- `docs/conversations/comic-file-organizer_BOOKMARKS.md` — copy of `comic-file-organizer/BOOKMARKS.md`.
- `docs/conversations/org_level_Scripts_FULL.md` — full transcript copy of `org_level_Scripts/README.md`.
- `docs/conversations/comics-suite_Action-Log.md` — copy of `comics-suite/docs/Action-Log.md`.

Other artifacts (found during scan)

- mylar3-test/comic_file_organizer/dfa/README_EXTRA.md
  - Path: mylar3-test/comic_file_organizer/dfa/README_EXTRA.md
  - Summary: Project-specific documentation / backup conversation for the DFA work (long form).

- .github/Project-Setup-Guide.md
  - Path: .github/Project-Setup-Guide.md
  - Summary: Repository-level project setup guide and appendices (will be updated to link to this documentation index).

Goals and next recommended steps

1. Use this DOCUMENTATION_INDEX.md as the single entry-point to find conversation logs and bookmarks.
2. Keep logs in their originating repos; add or update entries here for discoverability.
3. Add short README pointers inside each package (e.g., `comic-file-organizer/README.md`) that reference the local logs.
