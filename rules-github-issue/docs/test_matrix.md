# ZooCode GitHub Issue Mode — Comprehensive Test Matrix & Verification Checklist

## System Architecture & Role Definitions
* **Execution Agent (GitHub Issue Mode):** Reads XML prompts (`1_workflow.xml`, `2_best_practices.xml`, etc.) to parse user prompts, handle issue creation, search duplicates, coordinate code fixes, create Pull Requests, and manage workspace cleanup.
* **Mode Writer AI:** Updates and refines the core system prompt configuration files based on evaluation run feedback.
* **Architect / Oversight AI:** Evaluates live execution traces against protocol guardrails, identifies process defects, and maintains system verification matrices.

---

## Core Protocol Rules & Guardrails
* **Internal-Only Acceptance Criteria (AC):** Acceptance Criteria are extracted strictly for private scratchpad verification and **MUST NEVER** leak into public GitHub issue bodies.
* **Identity & Permission Resolution:** Resolve `STAKEHOLDER_USERNAME` via `git config user.email` and GitHub search API (`{email}+in:email`). Evaluate `CAN_MERGE` permission flags (`admin`, `write`, `maintain` vs. `read`).
* **Conditional Issue Assignment:** Assign `STAKEHOLDER_USERNAME` **ONLY** if an issue remains open without an immediate fix. Leave unassigned if an immediate code fix is initiated.
* **Mandatory Hard Stop Approval Gates:**
  1. **Gate #1:** Stop and wait for explicit human approval on drafted issue Markdown before calling `create_issue`.
  2. **Gate #2:** Stop and wait for explicit human approval before creating branches or attempting code modifications.
  3. **Gate #3:** Stop and wait for explicit human review of `git diff` and test suite execution in GitHub Issue Mode before calling `git push` or `create_pull_request`. Sub-modes (Code/Orchestrator) are strictly prohibited from pushing or creating PRs directly.
* **Branch Naming Standard:** Dedicated feature branches **MUST** strictly follow the pattern `issue-{number}-{short-slug}` (e.g., `issue-14-analytics-division-fix`). Standalone `issue-{number}` or generic prefixes (`fix/`, `feature/`) are prohibited.
* **Native Webhook Automation:** **NEVER** manually close issues via the API. Pull Request descriptions must end with standalone plain-text keywords (e.g., `Fixes #14`) on their own line to trigger native GitHub webhook closures.
* **Permission-Aware Merging:** Offer to execute PR merges via `merge_pull_request` **ONLY** if `CAN_MERGE` evaluates to `true`.
* **Workspace Hygiene & Lifecycle Completion:** A task **CANNOT** be marked as completed upon PR creation. The agent must restore the local workspace (`git checkout main && git pull`) and offer remote feature branch cleanup post-merge.

---

## Comprehensive Test Matrix

### Phase 1: Initialization & Identity Resolution

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-1.1** | Standard Identity Resolution | Valid `remote.origin.url`, `git config user.email` returns active email. | • Resolves `STAKEHOLDER_USERNAME` via GitHub API (`{email}+in:email`).<br>• Evaluates `CAN_MERGE` permission flag based on repo role. | PASS | PASS | **PASS** |
| **TC-1.2** | Unset/Missing Git Email | `git config user.email` returns empty string. | • Fallback: Sets `STAKEHOLDER_USERNAME` to repository owner.<br>• Prompts for manual override if user lookup fails. | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-1.3** | Invalid Git Remote URL | Invalid or missing `remote.origin.url`. | • Handles parsing error gracefully.<br>• Asks user to manually provide `owner/repo` details. | UNTESTED | UNTESTED | **UNTESTED** |

---

### Phase 2: Issue Drafting & Hard Approval Gate #1

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-2.1** | Internal AC Protection | Prompt contains explicit Acceptance Criteria. | • **CRITICAL:** Strips AC from public GitHub Markdown body.<br>• Stores AC in private scratchpad memory only. | PASS | PASS | **PASS** |
| **TC-2.2** | Gate #1 Stop (Draft Review) | Public issue draft formatted in Markdown. | • **HARD STOP:** Displays draft to user.<br>• **WAITS** for explicit confirmation before calling `create_issue`. | PASS | FAIL *(Bypassed draft pause)* | **FAIL** *(Regression)* |
| **TC-2.3** | User Rejects Issue Draft | User requests edits to the issue summary or steps. | • Revises Markdown internally.<br>• Re-presents draft and pauses again without calling API. | UNTESTED | UNTESTED | **UNTESTED** |

---

### Phase 3: Duplicate Detection & Creation Routing

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-3.1** | Duplicate Found | Similar issue/PR exists in repository. | • Intercepts creation.<br>• Presents choices: (a) Link as related, (b) Comment on existing, (c) Create new anyway. | PASS | N/A *(0 hits)* | **PASS** |
| **TC-3.2** | Semantic Duplicate Pre-Analysis *(New)* | Search API returns candidate matches. | • Provides a 1-sentence semantic comparison analyzing candidate matches before presenting choice menu. | PENDING | N/A *(0 hits)* | **PENDING** |

---

### Phase 4: Fix Coordination, Assignment, & Branching

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-4.1** | Gate #2 & Immediate Fix | User approves immediate fix attempt. | • **HARD STOP:** Asks user before modifying code.<br>• **Leaves issue UNASSIGNED**. | PASS | PASS | **PASS** |
| **TC-4.2** | Deferred Fix Execution | User declines immediate fix. | • **CONDITIONAL ASSIGNMENT:** Assigns `STAKEHOLDER_USERNAME` to open issue.<br>• Terminates session safely. | PASS | UNTESTED | **PASS** |
| **TC-4.3** | Strict Branch Naming | Branch creation step triggered. | • Enforces strict pattern: `issue-{number}-{short-slug}`.<br>• **REJECTS** standalone `issue-{number}` or `fix/` prefixes. | PASS | FAIL *(Created `issue-14`)* | **FAIL** *(Regression)* |

---

### Phase 5: Verification & Gate #3 (PR Submission)

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-5.1** | Native Webhook & PR Creation | Code edits and local tests completed. | • Creates Pull Request with plain-text keyword (`Fixes #X`).<br>• **NEVER** closes issue directly via API `update_issue`. | PASS | FAIL *(Closed issue via API)* | **FAIL** *(Regression)* |
| **TC-5.2** | Gate #3 Stop (Pre-Push Review) | Diff and test suite execution ready. | • **HARD STOP:** Returns control to GitHub Issue Mode.<br>• Displays diff/tests and **WAITS** for approval before `git push`/PR creation. | PASS | PASS | **PASS** |
| **TC-5.3** | Multi-Duplicate Sweep *(New)* | Multiple duplicate issues confirmed during resolution. | • Includes closing references (`Fixes #X, Fixes #Y`) for all confirmed duplicate issues in PR description and commit body. | PENDING | UNTESTED | **PENDING** |

---

### Phase 6: Permission-Aware Merging & Workspace Cleanup

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Pass 1 Status | Pass 2 Status | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-6.1** | Merge Execution (`CAN_MERGE = true`) | PR created and user has write/admin access. | • Prompts user to merge PR.<br>• Calls `merge_pull_request` upon confirmation to trigger automated issue closure. | PASS | UNTESTED | **PASS** |
| **TC-6.2** | Read-Only User (`CAN_MERGE = false`) | PR created but user lacks write access. | • Suppresses merge offer.<br>• Outputs PR URL and instructs user to request maintainer review. | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.3** | Workspace Restoration & Branch Cleanup | PR merged or session concluding. | • Switches checkout back to default branch (`git checkout main && git pull`).<br>• Deletes local and remote feature branches. | PASS | FAIL *(Skipped cleanup)* | **FAIL** *(Regression)* |