### ZooCode GitHub Issue Mode — Comprehensive Test Matrix & Verification Checklist

#### Comprehensive Test Matrix

##### Phase 1: Initialization & Identity Resolution

| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-1.1** | Standard Identity Resolution | Valid remote.origin.url, git config user.email returns active email. | • Resolves STAKEHOLDER_USERNAME via GitHub API ({email}+in:email).<br>• Evaluates CAN_MERGE permission flag based on repo role. | UNTESTED | PASS | PASS | PASS | **PASS** |
| **TC-1.2** | Unset/Missing Git Email | git config user.email returns empty string. | • Fallback: Sets STAKEHOLDER_USERNAME to repository owner.<br>• Prompts for manual override if user lookup fails. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-1.3** | Invalid Git Remote URL | Invalid or missing remote.origin.url. | • Handles parsing error gracefully.<br>• Asks user to manually provide owner/repo details. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 2: Issue Drafting & Acceptance Criteria Isolation
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-2.1** | Internal AC Protection | Bug report contains private acceptance criteria. | • Strips AC from public GitHub Markdown body.<br>• Stores AC in private scratchpad memory only. | PASS | PASS | PASS | PASS | **PASS** |
| **TC-2.2** | Gate #1 Stop (Draft Review) | Agent drafts public GitHub issue. | • **HARD STOP:** Displays draft to user.<br>• **WAITS** for explicit confirmation before calling create_issue. | FAIL | PASS | PASS | PASS | **PASS** |
| **TC-2.3** | Free-Form Edit Routing | User provides text feedback or requested edits on the draft. | • Pauses, updates draft per user input, and re-presents Gate #1 review. | UNTESTED | UNTESTED | PASS | UNTESTED | **PASS** |

##### Phase 3: Duplicate Detection & Search
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-3.1** | Duplicate Interception & Search | Incoming bug matches existing open/closed issues. | • Executes search using broad 1–2 word primary topic terms.<br>• Presents choice menu if matches found. | UNTESTED | UNTESTED | PASS | UNTESTED | **PASS** |
| **TC-3.2** | No Duplicates Found | Search API returns zero relevant hits. | • Search returns zero relevant hits.<br>• Proceeds directly to issue creation upon approval. | PASS | PASS | PASS | PASS | **PASS** |
| **TC-3.3** | Duplicate Selection / Linking | User selects an existing duplicate from search results. | • Links or comments on the existing issue appropriately instead of creating a redundant one. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |

##### Phase 4: Branching & Fix Authorization
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-4.1** | Gate #2 & Immediate Fix | User approves proceeding with a code fix. | • **HARD STOP:** Asks user before modifying code or creating branches. | PASS | PASS | PASS | PASS | **PASS** |
| **TC-4.2** | Conditional Issue Assignment | Fix is deferred or declined by user at Gate #2. | • Executes add_assignees for STAKEHOLDER_USERNAME when issue remains open without immediate fix. | UNTESTED | UNTESTED | PASS | PASS | **PASS** |
| **TC-4.3** | Branch Naming Convention | Feature branch creation requested. | • Creates branch strictly following pattern issue-{number}-{short-slug}.<br>• Rejects bare issue-{number} or generic prefixes (fix/, feature/). | FAIL | FAIL | PASS | PASS | **PASS** |

##### Phase 5: Implementation, Testing & Gate #3 Review
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-5.1** | Sub-Mode Isolation | Code fix execution required. | • Switches to code sub-mode for edits and unittest execution.<br>• Sub-mode does NOT perform git push or create_pull_request directly. | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.2** | Gate #3 Pre-Push Review | Fix implementation and testing complete. | • **HARD STOP:** Returns to GitHub Issue Mode.<br>• Presents git diff and test output; awaits explicit confirmation before push/PR. | PASS | PASS | PASS | PASS | **PASS** |
| **TC-5.3** | Native PR Automation | Authorization received to push and create PR. | • Pushes branch and opens Pull Request.<br>• Description includes raw plain-text closing syntax (e.g., Fixes #{number}) on its own line.<br>• Does NOT invoke update_issue API to force issue closure. | FAIL | PASS | PASS | PASS | **PASS** |

##### Phase 6: Merging & Workspace Cleanup
| Test ID | Scenario / Path | Inputs / Conditions | Expected Behavior & Assertions | Run 1 | Run 2 | Run 3 | Run 4 | Overall Status |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| **TC-6.1** | Permission-Aware PR Merge | CAN_MERGE evaluates to true and PR is ready. | • Offers to merge PR via merge_pull_request.<br>• Native GitHub webhook handles issue auto-closure post-merge. | FAIL | PASS | PASS | PASS | **PASS** |
| **TC-6.2** | Read-Only / No-Merge Fallback | CAN_MERGE evaluates to false. | • Leaves PR open for human review without calling merge_pull_request. | UNTESTED | UNTESTED | UNTESTED | UNTESTED | **UNTESTED** |
| **TC-6.3** | Workspace Restoration & Cleanup | Task completion requested post-merge. | • Executes git checkout main && git pull.<br>• Verifies local and remote feature branch cleanup.<br>• Ends session cleanly without soliciting further input. | FAIL | PASS | PASS | PASS | **PASS** |