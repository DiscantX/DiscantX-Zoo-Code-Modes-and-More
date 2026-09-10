# Architect Handoff — 2026-09-10 (Session 5)

## What this session did

1. Confirmed the session-4 duplicate-interception fix held (TC-2.4 now STABLE, 5/5).
2. Found and fixed (via Mode Writer brief, now confirmed working) two undefined-mechanics bugs in duplicate resolution: "Close/comment as duplicate" was spuriously creating-then-closing a new issue (TC-2.8); "Link" was silently reading code, running the full test suite, and completing without a clear statement to the user (TC-2.9). Both confirmed clean post-fix (R8, R9).
3. Began Orchestrator-delegated invocation testing (TC-0.2, previously UNTESTED — highest-leverage untested area identified this session). Confirmed gate integrity holds correctly *within* a delegated child task, including the decline path and lazy stakeholder resolution (R10, R11).
4. **Surfaced a severe, higher-priority finding (TC-0.3):** Orchestrator will independently spawn a second, ungated subtask to complete work a human explicitly declined inside a delegated child task — fully bypassing the audit-trail pipeline (no branch, no commit tracked, no PR, no Gate #3, no issue reference). This is structural, not a per-run fluke — Orchestrator's own reasoning trace explicitly shows the override decision.
5. Sent a Mode Writer brief for a new global `rules-orchestrator/` directory to address #4 (Orchestrator is a built-in mode with a hardcoded prompt, not editable via `custom_modes.yaml` — this is the first rules directory targeting a built-in mode rather than a custom one).
6. Noted an unverified identity anomaly: `git config --get user.email` returned a synthetic sandbox value (`roo@code.local`) during a delegated decline-path run, not Ficus's real email. Hypothesis: ZooCode's checkpoint mechanism may run this lookup against its own private git repo rather than the TestBed repo. Not yet isolated — see next steps.
7. Full [`rules-github-issue-docs/test_matrix.md`](rules-github-issue-docs/test_matrix.md) updated in-conversation with all R5–R11 results; ready to save over the existing file.

## Immediate next steps, in priority order

1. **Verify Mode Writer's `rules-orchestrator/` output**, then re-run the TC-0.3 decline scenario (BUG-2.1 or similar, Orchestrator-delegated, Gate #2 decline) to confirm Orchestrator now respects the decline and stops instead of re-delegating. This is the single highest-priority open item.
2. **Isolate the identity anomaly**: repeat a decline-path lazy-stakeholder-resolution trial at **Root invocation** (not Orchestrator-delegated) and check whether `git config --get user.email` resolves correctly there. Confirms or refutes the checkpoint-repo hypothesis and determines how much confidence TC-1.6 deserves going forward.
3. Once both above are resolved, resume **TC-0.4** (organic mode selection — no explicit delegation instruction) as originally sequenced.
4. Lower priority, still open: TC-3.7 (label matching, needs a repo with real labels seeded), TC-4.5/4.6, TC-5.4/5.6/5.7/5.9, TC-6.6, TC-7.1 (needs a standalone non-duplicate manual closure trial), TC-7.2.

## Repo state at end of session

- TestBed repo unchanged from R11 except: `auth.py`'s unauthorized direct edit (from the TC-0.3 incident) has been manually reverted by Ficus. BUG-2.1 is therefore live again in `auth.py`.
- Issues #1–#11 all exist on GitHub in their end-of-session states (see Run Ledger in [`rules-github-issue-docs/test_matrix.md`](rules-github-issue-docs/test_matrix.md) for specifics per issue).
- No file or GitHub reset occurred this session.

## Standing reminders for next session

- Mode Writer must never receive test IDs or bug catalog references — protocol-neutral prose only, as always.
- 3+ replications before drawing stability conclusions — TC-0.3's single-trial FAIL is being treated as high-confidence only because the model's own reasoning trace makes the mechanism explicit, not because of trial count.
- `rules-orchestrator/` is a new pattern (targeting a built-in mode). If it doesn't work as expected, the fallback lever is strengthening `github-issue` mode's own `attempt_completion` phrasing to more forcefully flag explicit declines — weaker guarantee, but doesn't depend on Orchestrator honoring an external rules directory it wasn't previously scoped to read.

## Additional Investigation: Git Identity Anomaly Root Cause & Resolution

1. **Resolved local git config anomaly**: Confirmed the synthetic sandbox email (`roo@code.local`) was located in the TestBed repo's `.git/config` (local scope, not global).
2. **Identified rule defect**: Traced to [`rules-github-issue/2_best_practices.xml`](rules-github-issue/2_best_practices.xml:19)'s instruction requiring explicit scope flags (`git config --local user.email`). The rule sets fallback identity *unconditionally* rather than checking if an identity is already configured, silently overwriting real user configs.
3. **Implications for test matrix**: TC-1.6 ("PASS" in R11) must be downgraded to **INCONCLUSIVE**, as email-search-miss trials tested against the synthetic `roo@code.local` placeholder rather than a genuine user email configuration.
4. **Mode Writer queue addition**: Update the fallback identity rule to check `git config --get user.email` first and only set a fallback if empty, avoiding unconditional overwrites.

## Detailed Investigation & Discussion Summary

### 1. Label Discovery Failure Analysis
- **Root Cause:** [`github-issue`](custom_modes.yaml:681) mode was previously instructed to query repository labels via GitHub MCP tools. However, the GitHub MCP server does not expose a `list_labels` or `get_labels` tool.
- **Fallback Limitation:** Relying on [`mcp--github--list_issues()`](rules-github-issue/1_workflow.xml:86) only returned labels attached to recently fetched issues (up to 30 issues on page 1), leaving empty label lists for new or sparsely tagged repositories.

### 2. Name vs. Description Semantic Matching
- Analyzed whether matching occurs solely against label names or if descriptions are read.
- Concluded that retrieving label definitions with both `name` and `description` (e.g., via JSON output) allows the LLM to read descriptions (e.g., `"Barrier affecting people with disabilities"` for `accessibility`) to achieve highly accurate semantic matches.

### 3. CLI vs. REST API vs. Issue Mining Comparison
- **GitHub CLI (`gh label list --json name,description`):** Instantly queries labels using local authentication; fails if `gh` is uninstalled or unauthenticated.
- **REST API (`GET /repos/{owner}/{repo}/labels`):** Universal fallback using HTTP utilities (`curl` / [`Invoke-RestMethod`](rules-github-issue/3_common_patterns.xml:18)).
- **Issue Mining (`list_issues`):** Incomplete and paginated (first 30 recent issues only); retained strictly as a tertiary fallback.

### 4. Policy Enhancements Discussed
- **New Label Proposals:** When no existing label matches, the agent now drafts 1–3 proposed new labels (name, color, description) for user approval at Hard Stop [`Gate #1`](rules-github-issue/1_workflow.xml:104) instead of defaulting to no label.
- **Multi-Label Assignment:** Enabled matching both a Primary Type label (`bug`, `enhancement`, `task`) and Secondary Contextual labels (`accessibility`, `documentation`, `good first issue`, `ui`).
- **Duplicate Search Pipeline:** Confirmed that [`mcp--github--search_issues()`](rules-github-issue/1_workflow.xml:35) searches the entire repository issue database via GitHub's backend index in a single query, avoiding client-side pagination overhead.

---

## Detailed Summary of Implemented Changes

1. **[`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:86):**
   - Added the multi-tier label discovery pipeline (CLI -> REST API -> `list_issues` fallback).
   - Updated session caching instruction to store label names and descriptions.
   - Added multi-label semantic matching instructions (Primary Type + Secondary Domain Context).
   - Added new label creation proposals and presentation at Hard Stop [`Gate #1`](rules-github-issue/1_workflow.xml:104).
   - Updated issue creation step to execute label creation via CLI/API upon explicit user approval.

2. **[`rules-github-issue/2_best_practices.xml`](rules-github-issue/2_best_practices.xml:9):**
   - Renamed and expanded best practice principle to **Once-Per-Session Label Retrieval & Multi-Label Semantic Matching**, covering multi-tier retrieval and user-approved label additions.

3. **[`rules-github-issue/3_common_patterns.xml`](rules-github-issue/3_common_patterns.xml:15):**
   - Updated `label_retrieval_and_semantic_matching` pattern with the multi-tier query steps, primary/secondary matching rules, and new label drafting logic.

4. **[`rules-github-issue/4_decision_guidance.xml`](rules-github-issue/4_decision_guidance.xml:11):**
   - Updated decision rule for session label retrieval to reference the multi-tier pipeline and multi-label proposals.

5. **[`rules-github-issue/5_examples.xml`](rules-github-issue/5_examples.xml:15):**
   - Updated workflow examples (`bug_report_to_pr_workflow` and `feature_request_workflow`) to demonstrate multi-label matching and new label drafting.

6. **[`rules-github-issue/6_error_handling.xml`](rules-github-issue/6_error_handling.xml:11):**
   - Added error scenarios for missing repository labels and primary discovery failures (CLI -> REST API -> issue mining cascade).

7. **[`rules-github-issue/7_communication.xml`](rules-github-issue/7_communication.xml:10):**
   - Updated [`Gate #1`](rules-github-issue/1_workflow.xml:104) communication scenario to explicitly include reviewing proposed new label names and descriptions.

8. **[`custom_modes.yaml`](custom_modes.yaml:687):**
   - Updated the `github-issue` mode roleDefinition and capabilities summary to reflect multi-tier label discovery and label creation proposals.
