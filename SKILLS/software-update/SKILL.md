---
name: software-update
description: Analyzes merged PRs/MRs from a GitHub or GitCode repository for a given time period and generates a structured software update report. Extracts software names, version numbers, and base OS versions from repository file path conventions. Use when user asks to "summarize software updates", "software update", provides a GitHub or GitCode repository URL with a time period, or needs a changelog-style report from a git repository. Not for GitLab, Bitbucket, or local repositories.
---

# Software Update

Analyzes merged Pull Requests (GitHub) or Merge Requests (GitCode) from a public repository for a specified time period, then generates a structured markdown update report grouped by software category.

## Workflow

### Step 1: Parse User Input

Extract from the user's request:
- `<repo-url>`: Full repository URL (GitHub or GitCode)
- `<start-date>` and `<end-date>`: Time period (e.g., "2025年2月" → `2025-02-01` to `2025-02-28`)
- `<output-path>`: Output path (default: `uploads/<repo-slug>-<YYYY-MM>.md`)

Detect platform from URL:

| URL pattern | Platform | PR reference format |
|---|---|---|
| `github.com/...` | GitHub | `#NNNN` |
| `gitcode.com/...` | GitCode | `!NNNN` |

Derive `<repo-slug>` from the last non-empty path segment of `<repo-url>`.

### Step 2: Delegate Analysis to Subagent

Spawn a `general-purpose` subagent with this prompt (substituting actual values):

```
Analyze merged PRs from <platform> repository <repo-url> merged between <start-date> and <end-date>.

Steps:
1. Clone (shallow): git clone --depth=500 <repo-url> /tmp/repo-<repo-slug>
2. Extract merge commits in the date range:
   git -C /tmp/repo-<repo-slug> log --merges \
     --format="%H|%ad|%s" --date=format:"%Y-%m-%d" \
     --after="<start-date>" --before="<end-date>"
3. For each merge commit hash, list changed files:
   git -C /tmp/repo-<repo-slug> show --stat <hash> | grep "Dockerfile\|\.yml\|\.md\|\.spec"
4. Parse Dockerfile paths using the convention (if present):
   <Category>/<software>/<version>/<base-os-version>/Dockerfile
   Extract: category, software, version, base-os-version
   If paths don't follow this convention, record the raw changed paths instead.
5. Classify PR type from commit subject (see classification rules below)
6. Extract PR/MR number from commit subject:
   - GitHub: looks like "(#NNNN)" or "Merge pull request #NNNN"
   - GitCode: looks like "!NNNN" in the subject
7. Clean up: rm -rf /tmp/repo-<repo-slug>
8. Return a table with columns:
   hash | date | pr-number | title | category | software | version | base-os-version | type
```

Wait for the subagent to return the structured data before proceeding.

### Step 3: PR Type Classification

| Commit subject pattern | Type |
|---|---|
| Contains `【自动升级】` | 自动升级 |
| Contains `【Bug修复】` or starts with `fix` / `Fix` | Bug 修复 |
| Adds a new path with no prior version directory | 新增镜像 |
| `feat:` or `Add ` prefix | 新增功能 |
| `chore:` or `docs:` prefix | 其他 |
| None of the above | 其他 |

### Step 4: Aggregate Statistics

From the subagent data, compute:
- Total merged PR/MR count
- Count per type
- List of software names per type (deduplicated)
- Count per base OS version (when available)

### Step 5: Generate Report

Read `references/report-template.md` for the full report structure.

Populate the template with aggregated data and write to `<output-path>`.

Ensure the output directory exists:
```bash
mkdir -p uploads
```

## Error Handling

- **Clone fails**: Verify the repository URL is public; report the exact git error to the user.
- **No merge commits found**: The repo may use squash merges or rebase strategy — inform the user and suggest checking the date range.
- **No Dockerfile paths found**: The repo doesn't use the `<Category>/<software>/<version>/<base-os>` convention; report raw commit data instead and omit the category breakdown section.
- **PR number not parseable**: Leave the PR column blank for that row; note the count in the report footer.
