# ZooCode GitHub Issue Mode — Project Overview and Instructions

## Project Overview

We are building a custom `GitHub Issue` mode for the **VS Code** extension **Zoo Code**. The intent is to create an audit trail of issues and implementations that are worked on by Zoo Code. The standard approach without this mode is for Zoo Code to work on whatever prompt the user gives it, and at the end the user can commit it should they choose. Issue creation in this circumstance must happen manually by the user.

Rather than this, `GitHub Issue Mode` will take the user's prompt, create an issue from it, optionally try to fix it in a new branch, make a pull request, and optionally merge it to main, cleaning up after itself by removing the now-stale branch.

### Zoo Code Modes

A mode in Zoo Code is a specialized AI persona configured with distinct system prompts, tool permissions, and model preferences for a specific development workflow. It defines exactly what an agent can do—such as writing code, debugging, or analyzing architecture—while restricting or granting access to file-editing and terminal capabilities. A mode is defined both by an entry in the user's `custom_modes.yaml` and by optional `rules` directories containing instructions.

While Markdown and text are the most common formats, the agent recursively reads any instruction files—including structured XML rule files—placed inside the `/rules-{modeSlug}/` directory. This applies whether rules are placed in global storage (e.g., `%USERPROFILE%/.roo`) or copied into a local workspace directory (e.g., `.zoo/rules-{modeSlug}/` or project root). Because Zoo Code inherently understands XML tags to handle its internal system execution, using XML files within these rule directories is a highly effective way to enforce strict constraints, and is the convention this project follows.

## Blind Testing & Dual-Repository

This project exists in two separate repositories:

- **[DiscantX-Zoo-Code-Modes-and-More](https://github.com/DiscantX/DiscantX-Zoo-Code-Modes-and-More)** — The `Modes` repo contains all of the user `DiscantX`'s custom modes. The `GitHub Issue` mode can be found as a subdirectory of this repo, in `rules-github-issue`. This repo is purposefully airgapped from the `GitHub Mode` agent, so that it is blind to all tests that are being run on it.
- **[GitHub TestBed](https://github.com/DiscantX/GitHubTestBed)** — The `TestBed Repo` contains the Python code that will be used to test the `GitHub Issue Mode` agent. The code intentionally contains bugs, so that we can point it at real issues during testing. Note that the goal isn't to test its ability to fix the bug, but rather its ability to adhere to the git/GitHub actions flow we are prescribing to it.

This is also the repository in which we will be creating the test issues.

## Role Definitions

- **Execution Agent (GitHub Issue Mode):** Reads XML prompts (`1_workflow.xml`, `2_best_practices.xml`, `3_common_patterns.xml`, `4_decision_guidance.xml`, `5_examples.xml`, `6_error_handling.xml`, `7_communication.xml`, etc.), as well as its relevant section of `custom_modes.yaml`, to parse user prompts, handle issue creation, search duplicates, coordinate code fixes, create Pull Requests, and manage workspace cleanup.
- **Mode Writer Mode:** Updates and refines the core system prompt configuration files based on evaluation run feedback. This is itself a Zoo Code mode that focuses on writing new modes. When providing prompts to this mode, provide them in prose. **Important:** This role has no awareness of the specific tests we are running, nor access to documents such as this `AGENTS.md`. Provide it only with high-level protocol directives (e.g., "Enforce a hard stop at Gate #1 before calling create_issue") rather than referencing specific test IDs or test matrix rows. Do not assume it has knowledge of the `test matrix` or the results of previous test passes.
- **Architect / Oversight AI:** Evaluates live execution traces against protocol guardrails, identifies process defects, and maintains system verification matrices. If you are an AI reading this, this is likely you.

---

## Test Matrix

The `Modes` repo contains a file at `rules-github-issue\docs\test_matrix.md` that contains a table of various scenarios, paths, and failure modes that we are testing against. While testing, the user will provide live updates to the `Architect AI` by providing a copy-paste of what the `GitHub Issue Mode` agent is doing whenever it stops at a "gate." When it stops, the Architect AI will provide an analysis of how well it has adhered to its system prompt (i.e., its `.xml` files). Use the `test_matrix.md` for this evaluation.

### Test Matrix Format

When providing the user with an updated version of the test matrix, you must output the Markdown inside a plain raw text code block (` ```markdown `) so it can be directly copied or downloaded as a raw file without rendering artifacts. Do not present it as pre-rendered Markdown text in normal chat output; this is a common formatting mistake that must be avoided.

### Core Protocol Rules & Guardrails

- **Internal-Only Acceptance Criteria (AC):** Acceptance Criteria are extracted strictly for private scratchpad verification and **MUST NEVER** leak into public GitHub issue bodies.
- **Identity & Permission Resolution:** Resolve `STAKEHOLDER_USERNAME` via `git config user.email` and GitHub search API (`{email}+in:email`). Evaluate `CAN_MERGE` permission flags (`admin`, `write`, `maintain` vs. `read`).
- **Conditional Issue Assignment:** Assign `STAKEHOLDER_USERNAME` **ONLY** if an issue remains open without an immediate fix. Leave unassigned if an immediate code fix is initiated.
- **Mandatory Hard Stop Approval Gates:**
  1. **Gate #1:** Stop and wait for explicit human approval on drafted issue Markdown before calling `create_issue`.
  2. **Gate #2:** Stop and wait for explicit human approval before creating branches or attempting code modifications.
  3. **Gate #3:** Stop and wait for explicit human review of `git diff` and test suite execution in GitHub Issue Mode before calling `git push` or `create_pull_request`. Sub-modes (Code/Orchestrator) are strictly prohibited from pushing or creating PRs directly.
- **Branch Naming Standard:** Dedicated feature branches **MUST** strictly follow the pattern `issue-{number}-{short-slug}` (e.g., `issue-14-analytics-division-fix`). Standalone `issue-{number}` or generic prefixes (`fix/`, `feature/`) are prohibited.
- **Native Webhook Automation:** **NEVER** manually close issues via the API. Pull Request descriptions must end with standalone plain-text keywords (e.g., `Fixes #14`) on their own line to trigger native GitHub webhook closures.
- **Permission-Aware Merging:** Offer to execute PR merges via `merge_pull_request` **ONLY** if `CAN_MERGE` evaluates to `true`.
- **Workspace Hygiene & Lifecycle Completion:** A task **CANNOT** be marked as completed upon PR creation. The agent must restore the local workspace (`git checkout main && git pull`) and offer remote feature branch cleanup post-merge.
