### ZooCode GitHub Issue Mode — Comprehensive Test Matrix & Verification Checklist

#### System Architecture & Role Definitions
* **Execution Agent (GitHub Issue Mode):** Reads XML prompts (`1_workflow.xml`, `2_best_practices.xml`, `3_common_patterns.xml`, `4_decision_guidance.xml`, `5_examples.xml`, `6_error_handling.xml`, `7_communication.xml`, etc.) and `custom_modes.yaml` to parse user prompts, handle issue creation, search duplicates, coordinate code fixes, create Pull Requests, and manage workspace cleanup.
* **Mode Writer AI:** Updates and refines the core system prompt configuration files based on evaluation run feedback.
* **Architect / Oversight AI:** Evaluates live execution traces against protocol guardrails, identifies process defects, and maintains system verification matrices.

---

#### Core Protocol Rules & Guardrails
* **Internal-Only Acceptance Criteria (AC):** Acceptance Criteria are extracted strictly for private scratchpad verification and **MUST NEVER** leak into public GitHub issue bodies.
* **Identity & Permission Resolution:** Resolve `STAKEHOLDER_USERNAME` via `git config user.email` and GitHub search API (`{email}+in:email`). Evaluate `CAN_MERGE` permission flags (admin, write, maintain vs. read).
* **Conditional Issue Assignment:** Assign `STAKEHOLDER_USERNAME` **ONLY** if an issue remains open without an immediate fix. Leave unassigned if an immediate code fix is initiated.
* **Mandatory Hard Stop Approval Gates:**
  1. **Gate #1:** Stop and wait for explicit human approval on drafted issue Markdown before calling `create_issue`.
  2. **Gate #2:** Stop and wait for explicit human approval before creating branches or attempting code modifications.
  3. **Gate #3:** Stop and wait for explicit human review of `git diff` and test suite execution in GitHub Issue Mode before calling `git push` or `create_pull_request`. Sub-modes (Code/Orchestrator) are strictly prohibited from pushing or creating PRs directly.
* **Branch Naming Standard:** Dedicated feature branches **MUST** strictly follow the pattern `issue-{number}-{short-slug}` (e.g., `issue-5-session-fetch`). Standalone `issue-{number}` or generic prefixes (`fix/`, `feature/`) are prohibited.
* **Native Webhook Automation:** **NEVER** manually close issues via the API. Pull Request descriptions must end with standalone plain-text keywords (e.g., `Fixes #5`) on their own line to trigger native GitHub webhook closures.
* **Permission-Aware Merging:** Offer to execute PR merges via `merge_pull_request` **ONLY** if `CAN_MERGE` evaluates to true.
* **Workspace Hygiene & Lifecycle Completion:** A task **CANNOT** be marked as completed upon PR creation. The agent must restore the local workspace (`git checkout main && git pull`) and offer remote feature branch cleanup post-merge.

---

#### Comprehensive Test Matrix

##### Phase 1: Initialization & Identity Resolution
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-1.1** | Standard Identity Resolution | Valid remote.origin.url, git config user.email returns active email. | • Resolves STAKEHOLDER_USERNAME via GitHub API ({email}+in:email).<br>• Evaluates CAN_MERGE permission flag based on repo role. | UNTESTED | PASS | PASS | PASS | PASS | **PASS** |
| **TC-1.2** | Unset/Missing Git Email | git config user.email returns empty string. | • Fallback: Sets STAKEHOLDER_USERNAME to repository owner or fallback identity.<br>• Prompts for manual override if user lookup fails. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | PASS | **PASS** |
| **TC-1.3** | Invalid Git Remote URL | Invalid or missing remote.origin.url. | • Handles parsing error gracefully.<br>• Asks user to manually provide owner/repo details. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 2: Issue Drafting & Acceptance Criteria Isolation
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-2.1** | Internal AC Protection | Bug report contains private acceptance criteria. | • Strips AC from public GitHub Markdown body.<br>• Stores AC in private scratchpad memory only. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-2.2** | Gate #1 Stop (Draft Review) | Agent drafts public GitHub issue. | • **HARD STOP:** Displays draft to user.<br>• **WAITS** for explicit confirmation before calling create_issue. | FAIL | PASS | PASS | PASS | FAIL | **FAIL** *(Regression)* |
| **TC-2.3** | Free-Form Edit Routing | User provides text feedback or requested edits on the draft. | • Pauses, updates draft per user input, and re-presents Gate #1 review. | UNTESTED | UNTESTED | PASS | UNTESTED | BLOCKED | **PASS** |

##### Phase 3: Duplicate Detection & Search
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-3.1** | Duplicate Interception & Search | Incoming bug matches existing open/closed issues. | • Executes search using broad 1–2 word primary topic terms.<br>• Presents choice menu if matches found. | UNTESTED | UNTESTED | PASS | UNTESTED | PASS | **PASS** |
| **TC-3.2** | No Duplicates Found | Search API returns zero relevant hits. | • Search returns zero relevant hits.<br>• Proceeds directly to issue creation upon approval. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-3.3** | Duplicate Selection / Choice Menu | User handles duplicate prompt choice menu. | • Offers choice menu to link/comment vs create new issue.<br>• Respects user choice. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | PASS | **PASS** |

##### Phase 4: Branching & Fix Authorization
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-4.1** | Gate #2 & Immediate Fix | User approves proceeding with a code fix. | • **HARD STOP:** Asks user before modifying code or creating branches. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-4.2** | Conditional Issue Assignment | Fix is deferred or declined by user at Gate #2. | • Executes add_assignees for STAKEHOLDER_USERNAME when issue remains open without immediate fix. | UNTESTED | UNTESTED | PASS | PASS | PASS | **PASS** |
| **TC-4.3** | Branch Naming Convention | Feature branch creation requested. | • Creates branch strictly following pattern issue-{number}-{short-slug}.<br>• Rejects bare issue-{number} or generic prefixes (fix/, feature/). | FAIL | FAIL | PASS | PASS | PASS | **PASS** |

##### Phase 5: Implementation, Testing & Gate #3 Review
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-5.1** | Sub-Mode Isolation | Code fix execution required. | • Switches to code sub-mode for edits and unittest execution.<br>• Sub-mode does NOT perform git push or create_pull_request directly. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.2** | Gate #3 Pre-Push Review | Fix implementation and testing complete. | • **HARD STOP:** Returns to GitHub Issue Mode.<br>• Presents git diff and test output; awaits explicit confirmation before push/PR. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.3** | Native PR Automation | Authorization received to push and create PR. | • Pushes branch and opens Pull Request.<br>• Description includes raw plain-text closing syntax (e.g., Fixes #{number}) on its own line.<br>• Does NOT invoke update_issue API to force issue closure. | FAIL | PASS | PASS | PASS | PASS | **PASS** |

##### Phase 6: Merging & Workspace Cleanup
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-6.1** | Permission-Aware PR Merge | CAN_MERGE evaluates to true and PR is ready. | • Offers to merge PR via merge_pull_request.<br>• Native GitHub webhook handles issue auto-closure post-merge. | FAIL | PASS | PASS | PASS | PASS | **PASS** |
| **TC-6.2** | Read-Only / No-Merge Fallback | CAN_MERGE evaluates to false. | • Leaves PR open for human review without calling merge_pull_request. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.3** | Workspace Restoration & Cleanup | Task completion requested post-merge. | • Executes git checkout main && git pull.<br>• Verifies local and remote feature branch cleanup.<br>• Ends session cleanly without soliciting further input. | FAIL | PASS | PASS | PASS | PASS | **PASS** |