### ZooCode GitHub Issue Mode — Comprehensive Test Matrix & Verification Checklist

#### Comprehensive Test Matrix

##### Phase 1: Initialization, Identity & Environment Resolution
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-1.1** | Standard Identity Resolution | Valid `remote.origin.url`, `git config user.email` returns active email | • Resolves `STAKEHOLDER_USERNAME` via GitHub API.<br>• Evaluates `CAN_MERGE` permission flag. | UNTESTED | PASS | PASS | PASS | PASS | **PASS** |
| **TC-1.2** | Missing Git Config Email | `git config user.email` returns empty; triggers owner/manual identity fallback | • Fallback: Sets `STAKEHOLDER_USERNAME` to repository owner or fallback identity.<br>• Prompts for manual override if user lookup fails. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | PASS | **PASS** |
| **TC-1.3** | Invalid Git Remote URL | Malformed origin URL; triggers error handling & manual input request | • Handles parsing error gracefully.<br>• Asks user to manually provide owner/repo details. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 2: Duplicate Search & Interception Routing
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-2.1** | Search Output: Clean | Search returns 0 candidates; proceeds directly to Gate #1 | • Search API returns zero relevant hits.<br>• Proceeds directly to issue creation upon approval. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-2.2** | Search Output: Duplicates Found | Search finds existing issues; halts and displays duplicate choice menu | • Executes search using broad primary topic terms.<br>• Halts and presents candidate choice menu. | UNTESTED | UNTESTED | PASS | UNTESTED | PASS | **PASS** |
| **TC-2.3** | Duplicate Choice A (Link/Comment) | User selects: "Link or comment on existing issue" | • Links/comments on existing issue appropriately without creating a redundant entry. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | PASS | **PASS** |
| **TC-2.4** | Duplicate Choice B (Skip & Fix) | User selects: "Skip issue creation and verify existing fix" | • Skips issue drafting phase and routes directly to fix verification / Gate #2. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-2.5** | Duplicate Choice C (Create Anyway) | User selects: "Create a new issue anyway" -> routes mandatory to Gate #1 | • Respects override request and routes directly to Gate #1 draft presentation. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | PASS | **PASS** |

##### Phase 3: Gate #1 — Public Issue Draft Approval
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-3.1** | Internal AC Protection | Bug report contains private acceptance criteria | • Strips AC from public GitHub Markdown body.<br>• Stores AC in private scratchpad memory only. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-3.2** | Gate #1 Hard Stop Isolation | Agent presents draft and pauses execution BEFORE calling `create_issue` | • **HARD STOP:** Displays draft to user.<br>• **WAITS** for explicit confirmation before calling `create_issue`. | FAIL | PASS | PASS | PASS | FAIL | **FAIL** *(Regression)* |
| **TC-3.3** | Gate #1 Option A: Approve As-Is | User approves draft as-is -> executes `create_issue` | • Calls `create_issue` API only after explicit user approval at Gate #1. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-3.4** | Gate #1 Option B: Free-Form Edits | User submits text edits -> agent updates draft & re-presents Gate #1 | • Pauses, updates draft per user input, and re-presents Gate #1 review. | UNTESTED | UNTESTED | PASS | UNTESTED | BLOCKED | **PASS** |
| **TC-3.5** | Gate #1 Option C: Cancel Draft | User cancels issue creation at Gate #1 | • Aborts issue creation workflow completely and terminates session cleanly. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 4: Gate #2 — Fix Attempt Authorization & Branching
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-4.1** | Gate #2 Hard Stop Isolation | Agent pauses after issue creation BEFORE modifying files/branches | • **HARD STOP:** Asks user before modifying code or creating branches. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-4.2** | Gate #2 Option A: Approve Fix | User authorizes fix -> creates branch matching `issue-{number}-{short-slug}` | • Switches to branch creation and code sub-mode. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-4.3** | Gate #2 Option B: Decline Fix | User declines fix -> assigns `STAKEHOLDER_USERNAME` & ends session | • Executes `add_assignees` for `STAKEHOLDER_USERNAME` when issue remains open without immediate fix. | UNTESTED | UNTESTED | PASS | PASS | PASS | **PASS** |
| **TC-4.4** | Branch Naming Standard | Feature branch creation requested | • Creates branch strictly following pattern `issue-{number}-{short-slug}`.<br>• Rejects generic prefixes (`fix/`, `feature/`). | FAIL | FAIL | PASS | PASS | PASS | **PASS** |

##### Phase 5: Implementation, Sub-Mode Isolation & Gate #3
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-5.1** | Sub-Mode Scope Boundaries | Code fix execution required | • Switches to code sub-mode for edits and unittest execution.<br>• Sub-mode does NOT perform git push or `create_pull_request` directly. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.2** | Gate #3 Hard Stop Isolation | Agent presents diff/test results and pauses BEFORE `git push`/PR creation | • **HARD STOP:** Returns to GitHub Issue Mode.<br>• Presents `git diff` and test output; awaits explicit confirmation before push/PR. | PASS | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.3** | Gate #3 Option A: Approve Push | User approves diff -> pushes branch and opens Pull Request | • Pushes branch and opens Pull Request. | FAIL | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.4** | Gate #3 Option B: Reject/Revise | User requests code revisions at Gate #3 | • Re-enters code sub-mode, applies requested changes, re-runs tests, and re-presents Gate #3. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-5.5** | Plain-Text Closing Syntax | PR description embeds standalone `Fixes #{number}` | • Embeds plain-text `Fixes #X` on its own line.<br>• Issue API is NOT called to close the issue manually. | FAIL | PASS | PASS | PASS | PASS | **PASS** |

##### Phase 6: PR Lifecycle, Merging & Workspace Cleanup
| Test ID | Decision Point / Scenario | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-6.1** | Merge Permission: `CAN_MERGE = false` | User lacks write permissions (`CAN_MERGE = false`) | • Leaves PR open for human review without calling `merge_pull_request`. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.2** | Merge Gate Option A: Execute Merge | User approves PR merge (`CAN_MERGE = true`) | • Offers to merge PR via `merge_pull_request`.<br>• Native GitHub webhook handles issue auto-closure post-merge. | FAIL | PASS | PASS | PASS | PASS | **PASS** |
| **TC-6.3** | Merge Gate Option B: Skip Merge | User declines auto-merge | • Leaves PR open in GitHub without executing `merge_pull_request`. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.4** | Workspace Restoration Protocol | Task completion requested post-merge | • Executes `git checkout main && git pull`.<br>• Verifies local and remote feature branch cleanup.<br>• Ends session cleanly without soliciting further input. | FAIL | PASS | PASS | PASS | PASS | **PASS** |