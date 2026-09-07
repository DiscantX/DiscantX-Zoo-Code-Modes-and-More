### ZooCode GitHub Issue Mode — Comprehensive Test Matrix & Verification Checklist

#### Instructions
Refer to the `AGENTS.md` in the root of this repository for instructions on how to use this document.

#### Comprehensive Test Matrix

##### Phase 1: Initialization & Identity Resolution
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-1.1** | Standard Identity Resolution | Valid `remote.origin.url`, `git config user.email` returns active email. | • Resolves `STAKEHOLDER_USERNAME` via GitHub API (`{email}+in:email`).<br>• Evaluates `CAN_MERGE` permission flag based on repo role. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-1.2** | Unset/Missing Git Email | `git config user.email` returns empty string. | • Fallback: Sets `STAKEHOLDER_USERNAME` to repository owner.<br>• Prompts for manual override if user lookup fails. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-1.3** | Invalid Git Remote URL | Invalid or missing `remote.origin.url`. | • Handles parsing error gracefully.<br>• Asks user to manually provide owner/repo details. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 2: Issue Drafting & Acceptance Criteria Isolation
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-2.1** | Internal AC Protection | Bug report contains private acceptance criteria. | • Strips AC from public GitHub Markdown body.<br>• Stores AC in private scratchpad memory only[cite: 8, 10]. | PASS | UNTESTED | UNTESTED | **IN PROGRESS** |
| **TC-2.2** | Gate #1 Stop (Draft Review) | Agent drafts public GitHub issue. | • **HARD STOP:** Displays draft to user.<br>• **WAITS** for explicit confirmation before calling `create_issue`[cite: 8, 10]. | FAIL | UNTESTED | UNTESTED | **FAIL** |
| **TC-2.3** | Free-Form Edit Routing | User provides text feedback or requested edits on the draft. | • Pauses, updates draft per user input, and re-presents Gate #1 review[cite: 9]. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 3: Duplicate Detection & Search
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-3.1** | Duplicate Interception & Search | Incoming bug matches existing open/closed issues. | • Executes search using broad 1–2 word primary topic terms.<br>• Presents choice menu if matches found[cite: 9]. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-3.2** | No Duplicates Found | Search API returns zero relevant hits. | • Search returns zero relevant hits.<br>• Proceeds directly to issue creation upon approval[cite: 8, 10]. | PASS | UNTESTED | UNTESTED | **IN PROGRESS** |
| **TC-3.3** | Duplicate Selection / Linking | User selects an existing duplicate from search results. | • Links or comments on the existing issue appropriately instead of creating a redundant one. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 4: Branching & Fix Authorization
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-4.1** | Gate #2 & Immediate Fix | User approves proceeding with a code fix. | • **HARD STOP:** Asks user before modifying code or creating branches[cite: 8, 10]. | PASS | UNTESTED | UNTESTED | **IN PROGRESS** |
| **TC-4.2** | Conditional Issue Assignment | Fix is deferred or declined by user at Gate #2. | • Executes `add_assignees` for `STAKEHOLDER_USERNAME` when issue remains open without immediate fix[cite: 9, 10]. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-4.3** | Branch Naming Convention | Feature branch creation requested. | • Creates branch strictly following pattern `issue-{number}-{short-slug}`.<br>• Rejects generic prefixes (`fix/`, `feature/`)[cite: 9, 10]. | FAIL | UNTESTED | UNTESTED | **FAIL** |

##### Phase 5: Pre-Push Validation & Pull Request Automation
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-5.1** | Test Suite Execution | Code fix applied locally. | • Runs unit test suite (`test_suite.py`) and verifies all tests pass prior to commit. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-5.2** | Gate #3 Pre-Push Review | Fix committed locally, ready for push and PR. | • **HARD STOP:** Presents `git diff` and test suite execution results.<br>• Waits for user review before calling `git push` or `create_pull_request`[cite: 8, 10]. | FAIL | UNTESTED | UNTESTED | **FAIL** |
| **TC-5.3** | Native PR Automation | Pull request creation. | • Embeds plain-text `Fixes #X` in PR description.<br>• Does NOT manually call Issues API to close the issue[cite: 8, 10]. | PASS | UNTESTED | UNTESTED | **IN PROGRESS** |

##### Phase 6: Merging & Workspace Restoration
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Overall Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-6.1** | Permission-Aware Merge Execution | PR created and tests verified. | • Prompts user to confirm merge.<br>• Calls `merge_pull_request` only if `CAN_MERGE` is true[cite: 8, 9, 10]. | FAIL | UNTESTED | UNTESTED | **FAIL** |
| **TC-6.2** | Deferred Merge Handling | User lacks merge permissions or defers merge. | • Leaves PR open for repository maintainer review without attempting unauthorized merge. | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.3** | Workspace Restoration & Cleanup | Task completed / PR merged. | • Restores local workspace (`git checkout main && git pull`).<br>• Cleans up local/remote feature branches[cite: 8, 9, 10]. | FAIL | UNTESTED | UNTESTED | **FAIL** |