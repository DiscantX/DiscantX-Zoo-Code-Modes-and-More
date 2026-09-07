### Comprehensive Diagnosis & Remediation Report for Zoo Code GitHub Issue Mode

Based on an exhaustive examination of [`AGENTS.md`](AGENTS.md:1), [`custom_modes.yaml`](custom_modes.yaml:684), [`rules-github-issue/docs/test_matrix.md`](rules-github-issue/docs/test_matrix.md:1), [`rules-github-issue/docs/bug_catalog.md`](rules-github-issue/docs/bug_catalog.md:1), and all XML rule definitions in [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:1) through [`rules-github-issue/7_communication.xml`](rules-github-issue/7_communication.xml:1), here is the detailed diagnosis of persistent test failures and the recommended remediation strategy.

---

### 1. Root Cause Breakdown

#### A. Direct Contradictions in [`custom_modes.yaml`](custom_modes.yaml:684) vs. XML Prompt Rules
1. **Branch Naming Standard (TC-4.3 Failure):**
   - [`custom_modes.yaml`](custom_modes.yaml:687) explicitly declares the capability: `Branch naming conventions ('issue-{number}')`.
   - In contrast, [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:82) and [`rules-github-issue/2_best_practices.xml`](rules-github-issue/2_best_practices.xml:37) mandate the regex `^issue-[0-9]+-[a-z0-9-]+$` (`issue-{number}-{short-slug}`) and state that bare `issue-{number}` is strictly forbidden.
   - Because `custom_modes.yaml` is loaded as the baseline system prompt, the agent receives contradictory instructions and defaults to `issue-{number}`.

2. **Issue Closure via API (TC-5.3 Failure):**
   - [`custom_modes.yaml`](custom_modes.yaml:686) states: `...and closing issues upon successful resolution... API / MCP integration (...closing issues)`.
   - In contrast, [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:66) forbids calling `update_issue` with `"state": "closed"`, requiring native GitHub PR webhook closures via plain-text `Fixes #{number}`.

3. **Stale Configuration Directives:**
   - [`custom_modes.yaml`](custom_modes.yaml:696) contains `customInstructions` referencing `write_to_file` and `.xml` mode editing (leaked from `mode-writer`), introducing unrelated context.

---

#### B. Sub-Mode Delegation Flaw (TC-5.2, TC-6.1, TC-6.3 Failures)
1. [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:87) instructs the agent to hand off fixes to `Code` or `Orchestrator` sub-modes.
2. Sub-modes operate under their own system prompts and do not load `/rules-github-issue/*.xml`.
3. When handed a fix task, standard development modes naturally modify files, run tests, commit changes, push, and open PRs or call completion without returning control to `github-issue` mode for **Gate #3** ([`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:99)), **Phase 6 Merge Evaluation** ([`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:132)), or **Workspace Cleanup** (`git checkout main && git pull`).

---

#### C. Human-in-the-Loop Gating Race Condition (TC-2.2 & TC-5.2 Failures)
1. Gate rules ("HALT EXECUTION") rely on text instructions rather than structured tool enforcement.
2. When the LLM generates markdown drafts or prepares commits, it frequently invokes MCP tools ([`create_issue`](rules-github-issue/1_workflow.xml:45), `git push`, `create_pull_request`) in the same turn before receiving user input.

---

#### D. Terminal Step Bias & Phase 6 Neglect (TC-6.1 & TC-6.3 Failures)
1. Pre-trained LLM behavior treats opening a Pull Request as the completion of a coding task.
2. Phase 6 is placed at the end of large, heavily repeated XML files ([`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:125) and [`rules-github-issue/2_best_practices.xml`](rules-github-issue/2_best_practices.xml:80)), leading to attention decay where the model calls completion tools prematurely.

---

### 2. Strategic Recommendations

1. **Keep Execution in Single Mode:** `github-issue` mode already has `read`, `edit`, `command`, and `mcp` tool groups configured in [`custom_modes.yaml`](custom_modes.yaml:691). Eliminating sub-mode switching avoids context loss and guarantees that all gate checks and cleanup steps remain strictly in scope.
2. **Standardize Gating with `ask_followup_question`:** Replace ambiguous "HALT" prose with structured tool prompts at Gate #1 (Draft Review), Gate #2 (Fix Approval), Gate #3 (Pre-Push Review), and Phase 6 (Merge Confirmation).
3. **Harmonize `custom_modes.yaml`:** Align [`custom_modes.yaml`](custom_modes.yaml:684) with the strict regex branch naming (`issue-{number}-{short-slug}`) and webhook-driven PR lifecycle.
4. **Streamline & Consolidate XML Prompts:** Reduce prompt bloat and negative repetitions across the 7 XML files into concise, positive state-machine instructions.

---

### 3. Actionable File-by-File Changes

#### 1. Update [`custom_modes.yaml`](custom_modes.yaml:684)
```yaml
  - slug: github-issue
    name: 🐙 GitHub Issue Mode
    roleDefinition: |-
      You are Roo Code, a GitHub Issue and Lifecycle Management Specialist. You specialize in copyediting bug reports and task descriptions into well-structured GitHub issues, searching for duplicates, implementing verified code fixes on dedicated feature branches (issue-{number}-{short-slug}), opening rich Pull Requests with native webhook closing keywords (Fixes #X), executing permission-aware merges, and restoring clean workspace state.
      Your expertise includes:
      - Public GitHub Issue formatting (excluding internal Acceptance Criteria)
      - Git remote URL parsing and user permission evaluation (CAN_MERGE)
      - Strict branch naming conventions (^issue-[0-9]+-[a-z0-9-]+$)
      - Strict human approval gates (Gate #1 Draft, Gate #2 Fix Approval, Gate #3 Pre-Push Review)
      - Automated GitHub PR webhook integration (NEVER closing issues manually via API)
      - Post-merge workspace hygiene (git checkout main && git pull and branch deletion)
    whenToUse: Use this mode when you need to turn a bug report or task description into a formal GitHub issue, create it on GitHub, search for similar existing issues, implement a verified fix, create a Pull Request with automated webhook closing keywords, handle permission-aware PR merges, and restore workspace state.
    description: Create, track, fix, PR, and merge GitHub issues with automated workflows
    groups:
      - read
      - edit
      - command
      - mcp
    source: global
    customInstructions: |
      Always execute all phases directly within github-issue mode without delegating to sub-modes. Use ask_followup_question at every approval gate (Gate #1, Gate #2, Gate #3, and Phase 6 Merge). Always restore the local workspace via `git checkout main && git pull` before completing tasks.
```

#### 2. Update [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:81)
- Remove the sub-mode delegation in [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:87) and perform code edits directly using `edit_file` / `search_replace` and tests via `execute_command`.
- Enforce explicit `ask_followup_question` halts at Gate #1, Gate #2, and Gate #3 before tool calls.

#### 3. Update [`rules-github-issue/1_workflow.xml`](rules-github-issue/1_workflow.xml:125) Phase 6 Execution
Enforce an explicit linear sequence for Phase 6:
```xml
<phase name="phase_6_post_merge_hygiene">
  <step number="1">Evaluate CAN_MERGE flag.</step>
  <step number="2">If CAN_MERGE == true, ask user via ask_followup_question to confirm merge.</step>
  <step number="3">If approved, call mcp--github--merge_pull_request(merge_method='squash').</step>
  <step number="4">Execute command: git checkout main &amp;&amp; git pull</step>
  <step number="5">Execute command: git branch -d issue-{number}-{short-slug} &amp;&amp; git push origin --delete issue-{number}-{short-slug}</step>
  <step number="6">Only after steps 1-5 succeed, call attempt_completion tool.</step>
</phase>
```