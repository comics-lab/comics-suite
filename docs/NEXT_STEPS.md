# Next Steps — Actionable To-Do for comics-lab

This document captures recommended, prioritized next steps based on the documentation artifacts and scans performed.

Top priorities (short term)

1. CI: Add a lightweight GitHub Actions workflow to run pytest across repositories that include tests (start with `comic-file-organizer` and `comic-file-organizer/tests`).
   - Create `.github/workflows/python-tests.yml` that sets up Python, installs `pytest`, and runs tests.
   - Goal: ensure the `comic-file-organizer` tests remain passing in CI.

2. Preserve transcripts in `docs/conversations/` (done) and add a short index entry to each package README pointing to `docs/DOCUMENTATION_INDEX.md` (done for `comic-file-organizer` and `org_level_Scripts`).

3. Decide move vs copy policy
   - Recommendation: copy the canonical conversation into `docs/conversations/` and keep the original file in-place as a package-local record. This preserves discoverability while not breaking existing local references.

Medium priorities (next sprint)

4. Update `.github/Project-Setup-Guide.md` with links to the new `docs/` index and add a short section explaining how to add new conversation artifacts (done: pointer added).

5. Create a `docs/README.md` describing the docs structure and conventions (who may add transcripts, naming conventions, and retention policy).

6. Add small helper scripts to regenerate the `docs/DOCUMENTATION_INDEX.md` automatically from a set of patterns (optional).

Lower priorities (later)

7. Consider importing original upstream repositories (like DFA) via `git subtree` or `git filter-repo` if preserving commit history is important.

8. Add cross-repo CI that runs integration tests for components that interact (e.g., `comic-file-organizer` + `mylar3-sanity`), once stable.

9. Create a small docs-lint CI check that ensures each package README includes a pointer to `docs/DOCUMENTATION_INDEX.md`.

How I can help next (pick any)

- I can create the CI workflow skeleton for pytest and open a PR.
- I can add `docs/README.md` describing conventions and a template for adding transcripts.
- I can copy additional transcripts or bookmarks into `docs/conversations/` if you point me at them.

Priority estimates

- Short term items (1–3): ~1–2 hours to implement and test locally.
- Medium items (4–6): ~2–4 hours to draft docs and helper scripts.
- Lower items: larger planning; estimate on request.
