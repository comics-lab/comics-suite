# Forking and Integrating External Projects

**Date:** 2025-10-21  
**Audience:** comics-lab organization maintainers  

---

## Overview

This document describes how to pull external GitHub projects into the comics-lab organization, whether as clean imports, selective integrations, or full forks.

---

## Architecture Decision: Top-Level vs. Subdirectory

**Recommendation: Top-level repositories**

External projects should be added as separate top-level repositories in the comics-lab organization, not in subdirectories like `forks/`.

### Why Top-Level

1. **GitHub organization model**: Each repository should be a top-level entity
2. **Consistency**: Matches existing structure (cbz-doctor, comicbook-core, etc.)
3. **Independence**: Allows each project its own:
   - Git history and branches
   - CI/CD pipelines
   - Issue tracking
   - Documentation
   - Release cycle
4. **Clarity**: Immediately visible in organization directory listing

### Example Structure

```
comics-lab/
├── comicbook-core/          (original)
├── cbz-doctor/              (original)
├── mylar3-sanity/           (original)
├── external-tool-name/      (external/forked)
├── another-project/         (external/forked)
└── comics-suite/            (meta)
```

---

## Import Strategies

### Strategy 1: Clean Import (Recommended for Most Cases)

Import only the current working code without full git history.

**Steps:**

1. Clone the original repo:
   ```bash
   git clone https://github.com/original-owner/project-name.git
   cd project-name
   ```

2. Check available branches:
   ```bash
   git branch -a
   ```

3. Create empty repository in comics-lab on GitHub (via web UI or CLI):
   ```bash
   gh repo create comics-lab/project-name --public
   ```

4. Change remote and push current state:
   ```bash
   git remote set-url origin git@github.com:comics-lab/project-name.git
   git push -u origin main --force
   ```
   (Replace `main` with the actual branch name if different, e.g., `master`)

5. Optional: Rename branch to `main` if needed:
   ```bash
   git branch -m main
   git push -u origin main --force
   ```

**Result:** Fresh git history starting from import point, no legacy branches/tags.

---

### Strategy 2: Full Mirror (All History, Branches, Tags)

Import everything from the original repo.

```bash
git clone --mirror https://github.com/original-owner/project-name.git
cd project-name.git
git push --mirror https://github.com/comics-lab/project-name.git
```

**Result:** Complete historical record, all branches and tags preserved.

---

### Strategy 3: Selective Import (Cherry-Pick Specific Components)

Extract only the code and features you want.

**Steps:**

1. Clone the original repo to a temporary directory:
   ```bash
   git clone https://github.com/original-owner/project-name.git temp-clone
   cd temp-clone
   ```

2. Delete unwanted files/directories:
   ```bash
   rm -rf unwanted_dir/ deprecated_module.py
   ```

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Import: extracted core functionality from upstream"
   ```

4. Change remote and push:
   ```bash
   git remote set-url origin git@github.com:comics-lab/project-name.git
   git push -u origin main --force
   ```

**Result:** Only desired code imported, clean slate to build from.

---

## Maintaining Upstream Sync (Optional)

If you want to track the original project for future updates:

```bash
git remote add upstream https://github.com/original-owner/project-name.git
```

**Later, to sync with upstream:**

```bash
git fetch upstream
git merge upstream/main  # or rebase, depending on workflow
```

---

## Managing GitHub Actions / CI-CD

External projects often include workflows that trigger on push.

### Find Running Workflows

**Via GitHub UI:**
- Repository → **Actions** tab

**Via CLI:**
```bash
gh run list --repo comics-lab/project-name
```

### Stop Running Workflows

**Via GitHub UI:**
- Click running workflow → **Cancel workflow**

**Via CLI (cancel all in-progress):**
```bash
gh run list --repo comics-lab/project-name --status in_progress --json databaseId -q '.[].databaseId' | xargs -I {} gh run cancel {} --repo comics-lab/project-name
```

### Disable Workflows

**Option 1: Disable Actions entirely**
- Repository **Settings** → **Actions** → **General** → "Disable actions"

**Option 2: Remove workflows**
```bash
rm -rf .github/workflows/
git add .
git commit -m "Remove upstream CI/CD workflows"
git push
```

**Option 3: Customize workflows**
- Edit `.github/workflows/*.yml` files to match comics-lab standards

---

## Post-Import Checklist

After importing an external project:

- [ ] Create empty repo in GitHub comics-lab organization
- [ ] Clone and import (using appropriate strategy above)
- [ ] Verify all code pushed successfully
- [ ] Check and manage GitHub Actions workflows
- [ ] Update LICENSE if needed (should be MIT for comics-lab)
- [ ] Add README describing origin and relationship to comics-lab
- [ ] Update `PROJECT-INDEX.md` in comics-suite/docs
- [ ] Document any breaking changes or modifications
- [ ] Add to organization project board if applicable

---

## Documentation & Attribution

### README Template for Imported Projects

```markdown
# project-name

[Original description]

## Source & Attribution

Imported into **comics-lab** from [original-owner/project-name](https://github.com/original-owner/project-name).

### Changes Made
- [List any modifications, deletions, or customizations]

### Upstream Sync
This repository may receive updates from upstream. To sync:
```bash
git fetch upstream
git merge upstream/main
```
```

### Update PROJECT-INDEX.md

Add to the appropriate section:

```markdown
- **project-name** - [Description]
  - Location: `./project-name/`
  - Source: Forked from [original-owner/project-name](https://github.com/original-owner/project-name)
  - Dependencies: [list]
  - Purpose: [description]
```

---

## Common Issues

### SSH Key Issues
If you see: `Permission denied (publickey)` or similar

- Ensure SSH key is added to your GitHub account
- Test: `ssh -T git@github.com`
- Use HTTPS as fallback: `git@github.com:` → `https://github.com/`

### Repository Not Found
If you see: `ERROR: Repository not found`

- Verify repo exists in GitHub organization
- Check SSH URL format (colon, not slash): `git@github.com:org/repo.git`
- Verify you have push access to the organization

### Branch Name Mismatch
If you see: `error: src refspec main does not match any`

- Check current branch: `git branch -a`
- Push the correct branch name: `git push -u origin master` (or whatever branch exists)
- Or rename branch first: `git branch -m main`

---

## Action Log

- 2025-10-21 — Initial guide created with import strategies and CI/CD management

---

*End of Document*
