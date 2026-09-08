# Architect AI Handoff — ZooCode GitHub Issue Mode

**Date of this session:** 2026-09-07
**Purpose:** Carry-forward synthesis for the next conversation. Nothing in this session has been sent to Mode Writer yet — all Mode Writer briefs below are still pending, not completed.

---

## 1. Project Refresher (see `AGENTS.md` for full detail)

- **Two repos:** `Modes` repo (`rules-github-issue/*.xml`, `custom_modes.yaml`, test matrix, bug catalog) is airgapped from the `TestBed` repo (seeded-bug Python app used as realistic test prompts). This keeps the execution agent blind to expected answers.
- **Roles:** Execution Agent (`github-issue` mode, reads the XML rules) → Mode Writer mode (edits the XML rules; has **no** visibility into test IDs, the bug catalog, or `AGENTS.md` — must only receive protocol-level prose asks) → Architect/Oversight AI (me — evaluates live gate traces against the test matrix).
- **Core protocol:** raw bug report → drafted public issue (AC stripped) → Gate #1 → `create_issue` → duplicate search → Gate #2 (attempt fix?) → branch `issue-{number}-{short-slug}` → fix → Gate #3 (review diff/tests) → push → PR with `Fixes #N` → Phase 6 (CAN_MERGE eval, merge, `git checkout main && git pull`, branch cleanup) → completion.
- **Prior tool:** Gemini was Architect before this session; migration to Claude was prompted partly by Gemini losing context on long trace-based test matrix updates.

---

## 2. Housekeeping / Process Decisions Made This Session

1. **Reset taxonomy** (for the Run Ledger going forward): distinguish **Files reset** (TestBed source restored to seeded-bug state) / **GitHub reset** (issues+PRs wiped, files untouched) / **Full reset** (both) / **Unchanged from prior run**. Log this per run.
2. **Run Ledger** introduced — a running log of Run ID, date, entry point (Root vs Orchestrator-delegated), repo state, bug/prompt used, and which TCs were targeted. This was previously missing and made it hard to know what a given run was even testing.
3. **Overall Status computation changed**: now = verdict of the **most recent** run for that TC (not an aggregate that could hide a regression depending on run order). Added a companion **Stability** column: `STABLE` / `REGRESSED` (passed once, later failed) / `FLAKY` (alternates repeatedly) / `N/A` (fewer than 2 runs).
4. **Incremental scoring going forward**: score each gate trace as it's pasted, immediately, rather than reconstructing the whole matrix from memory at the end of a long run. If the actual `test_matrix.md` file is uploaded at the start of a run, edits should be applied to it directly rather than regenerated from scratch. This is the main fix for the Gemini context-loss problem.
5. **Full test matrix reset performed** (see Section 5) — all prior Run 1–5 history retired given how much has changed since Gemini's tenure. Reasoning: cheap to re-baseline now vs. carrying forward stale/uncertain history.
6. **Bug catalog note:** `config.py` (BUG-1.1, BUG-1.2) and `auth.py` (BUG-2.1, BUG-2.2) in the current TestBed files are **already fixed** — the buggy code described in `docs/bug_catalog.md` is not present. If a test run points at one of these prompts, nothing will reproduce. Either reset TestBed files before using these prompts again, or pick a different still-broken bug (BUG-3.x through BUG-6.x all still contain their seeded defects, per direct source inspection this session).
7. **Standing Mode Writer instruction (to include in every future brief):** explicitly ask Mode Writer to confirm whether `custom_modes.yaml`'s `roleDefinition`/`whenToUse`/`groups` need a matching update whenever a change affects capabilities, role, or triggering conditions — Mode Writer has repeatedly neglected this file in the past.
8. **`Comprehensive_Diagnosis_and_Remediation.md` is stale.** Its `custom_modes.yaml` contradiction findings (branch naming, issue closure) have already been fixed in the current file. Its sub-mode delegation elimination recommendation was **deliberately not applied** — mode hand-off is a valued Zoo Code feature and should be preserved. The doc's lessons (esp. the custom_modes.yaml sync point above) remain valid; the specific diagnosis is outdated.

---

## 3. Zoo Code Architecture Findings (from AGENT_LOOP.md + docs/architecture/* + PR history research)

These came from reading `apps/cli/docs/AGENT_LOOP.md`, `docs/architecture/task-lifecycle-model.md`, `docs/architecture/native-tool-call-parser-scoping-model.md`, and searching Zoo-Code-Org/Zoo-Code PR history. **Important: this research was done via public GitHub search/fetch, not direct codebase access — treat as well-sourced but not exhaustive.**

### 3a. Ask types and gate enforcement
- All agent activity is a stream of `ClineMessage`s; type `ask` (non-partial) **halts the agent loop** until a response arrives — this applies structurally, at the loop level, to interactive asks generally.
- Ask categories: `tool`, `command`, `browser_action_launch`, `use_mcp_server` (all "Approve/Reject" style) vs. `followup` (our `ask_followup_question` — requires a real text/multi-choice answer). Per the docs, both categories are "Interactive Asks → WAITING_FOR_INPUT" and both block the loop the same way structurally.
- **User-confirmed nuance (important, corrects an earlier over-broad claim in this session):** MCP tool auto-approval (e.g., GitHub MCP's `search_repositories` set to "always allow" vs. `create_issue`/`create_repositories` requiring a click) is a **separate mechanism from our Hard Stop Gates**. Our gates ride entirely on `ask_followup_question` (a `followup` ask), not on whether the eventual `create_issue`/`create_pull_request`/`merge_pull_request` call itself is auto-approved. **Do not conflate these two in future analysis** — this was a mistake made and corrected during this session.
- **Most likely real explanation for gate violations (e.g., a `create_issue` call appearing without proper prior review):** the model skips `ask_followup_question` and proceeds straight to the MCP tool call, and a human clicking "Approve" on that tool's own execution-approval popup gets mistaken for (or actually substituted for) the intended content-review step. These are **not equivalent events** — clicking approve on a tool call is not the same as being shown drafted Markdown and asked "does this look right?" via `ask_followup_question`.
  - **→ Not yet sent to Mode Writer.** Proposed rule: *the tool's own execution-approval prompt must never be treated as satisfying the `ask_followup_question` content-review requirement at Gates #1/#2/#3 — the review step must complete, with an explicit response, before the tool call is even attempted.*
- **"Timed prompts with auto-defaults" exists** in Zoo Code's `PromptManager` (per AGENT_LOOP.md's component list) — some ask types may auto-resolve to a default option after a timeout in some client configurations. User has this explicitly **disabled**, but other users/environments may not.
  - **Actionable, high-priority finding:** if this setting is on, it always picks the **first-listed option**. Checked all four gates in `1_workflow.xml` — **every single one currently lists the "proceed" action first** (e.g., Gate #1: `["Approve and create issue", "Request edits to draft", "Cancel"]`). If a timeout ever fires, every gate in this protocol currently defaults toward action, not safety.
  - **User's explicit ruling on this (do not re-litigate):** do **not** blanket-reorder every gate to put the cautious option first — some users deliberately want auto-accept-and-proceed behavior, that's the point of the feature for them. Only reconsider ordering specifically where an action is **genuinely destructive/irreversible** (the user did not commit to changing anything here yet, just flagged the principle). **This is not yet a Mode Writer action item** — needs your judgment call on which specific gate(s), if any, actually rise to "truly destructive" before drafting anything.

### 3b. Mode-level tool restriction (hard gate — confirmed real)
- `filterNativeToolsForMode` and a `ModeConfig.allowedMcpServers: string[]` field exist and are enforced by an execution-layer check (referenced as `validateToolUse` in a PR touching Gemini tool-calling, which noted "the execution layer remains the final guard for mode-disallowed tools" even when a provider doesn't respect restrictions). This confirms mode-level tool restriction is structural, not prose.
- **Open/unconfirmed granularity question:** evidence found is for **server-level** allowlisting (whole MCP servers in/out), not confirmed **tool-level** restriction within one server (e.g., allowing GitHub MCP's `search_issues` but blocking `create_issue` within the same connector). The `edit` group's `fileRegex` scoping (seen in Mode Writer's own `custom_modes.yaml` entry) shows fine-grained restriction is possible for at least one tool category, but this hasn't been confirmed for MCP tool groups specifically.
  - **Implication:** a "draft-only mode" / "execute mode" split (two cooperating modes, one lacking write-capable GitHub tools entirely) is architecturally plausible but its exact granularity is unverified. Worth testing directly or asking Mode Writer to investigate before committing to a redesign — **do not design around this until confirmed**.

### 3c. Task delegation / Orchestrator-invoked execution
- From `task-lifecycle-model.md`: delegation (`ClineProvider.delegateParentAndOpenChild`) marks the parent as `delegated` with an `awaitingChildId`; parent only resumes via `reopenParentFromDelegation`, triggered by child completion.
- Current behavior (not yet changed): the parent is **dormant/not actively processing** while a delegated child runs — not proven "suspended" in the sense of losing state, but not concurrently live either. True parent-stays-live-during-child-run ("fan-out") is a **planned future feature**, tracked as open issues #369/#372, not yet implemented.
- **Clarified interpretation (per user, confirmed correct):** this is about **process-level concurrency** (can the parent do anything else while the child runs — currently no), **not** about conversational memory loss. The parent does rehydrate its own prior state/history when it resumes (the test-layering section explicitly mentions "task creation and rehydration, persisted parent-child state" as covered). This does **not** mean Orchestrator "forgets" or has to reprocess from scratch — it means it isn't multitasking during delegation. Not directly relevant to gate integrity questions but worth remembering accurately if it comes up again.
- **Implication for TC-0.2 (Orchestrator-delegated invocation):** since the parent isn't live/processing during delegation, it has no mechanism to intercept or mediate the child's `ask_followup_question` calls — they most likely surface directly to the human the same as a root invocation. This is a **reasonable prior, not proof** — TC-0.2 should still be run for real. Also note issue #921: delegation is supposed to bind an "immutable execution-context snapshot" of mode/profile state at delegation time, which is reassuring for `github-issue` mode's rules staying correctly scoped when invoked as a child task — also not yet directly tested.
- `native-tool-call-parser-scoping-model.md` was checked and found **not relevant** to this project (it's about correctly isolating fragments of two overlapping streamed tool calls, a different bug class entirely).

---

## 4. Real-World Use Cases Identified as Gaps (not yet built, not yet in Mode Writer queue)

1. **Fix an existing issue (`#N`) directly** — user references an issue number/URL instead of filing a new bug report. Sketch discussed:
   - Fetch issue via `get_issue`; skip drafting phase and Gate #1 entirely (nothing new to approve); skip duplicate search (target already known).
   - Fold a lightweight "here's what I understand from issue #N, confirm before I proceed" check into the existing Gate #2 rather than inventing a fourth gate.
   - Private Acceptance Criteria must be inferred from the fetched issue body/comments (no user-typed bug report to extract them from) — must stay private as usual.
   - Everything from fix_coordination onward reuses existing phases unchanged.
   - **Open decision, not yet made by user:** assignment logic if fix is declined — assign nobody, assign the invoking user, or ask explicitly? (Architect leans toward "ask explicitly" since identity is genuinely ambiguous here — issue may be filed by a stranger — but this is not decided.)
   - This also subsumes what was originally miscategorized as TC-2.4 ("Skip & Fix") in the old test matrix — that option doesn't exist in current `1_workflow.xml` and was a leftover/preview of this feature, now retired from Phase 2 and folded in here instead.
2. **Feature/enhancement request template** — current public issue template (Summary/Steps to Reproduce/Expected/Actual) is bug-shaped and doesn't fit a feature ask well. Needs a parallel template.
3. **Resuming a previously-declined issue** in a later session (was assigned to stakeholder, no fix attempted at the time) — not yet designed.
4. Smaller/lower-priority gaps also flagged: dirty working tree at start, non-GitHub remotes (should fail gracefully), labels/milestones/project-board assignment on creation.

None of these have been turned into Mode Writer briefs yet.

---

## 5. Test Matrix — Full Reset

The matrix was reset to all-UNTESTED this session, restructured with the Run Ledger, Stability column, corrected Phase 2 (aligned to the actual three duplicate-handling options in `1_workflow.xml` — the old TC-2.3–2.5 numbering didn't match reality), a new Phase 0 for invocation context, and ~14 new test cases covering gaps identified this session (fix-verification failure, draft override, shell-chaining rejection, adversarial sub-mode push, branch collision, multiple-duplicate handling, closed-vs-open duplicate, merge-blocked-despite-permission, etc.).

**Full current matrix content was generated in this session and should be saved to `rules-github-issue/docs/test_matrix.md`, replacing the existing file.** (Not re-duplicated in full here to keep this handoff doc manageable — if the next conversation doesn't have that matrix content, ask for it to be regenerated from this handoff's Section 5 description, or re-paste it from this session's transcript before it's lost.)

**Row count went from 13 to 27 TCs.** Recommendation made: don't try to re-walk everything in one marathon session — pick a handful of TCs per run using the Run Ledger to track partial coverage.

**Status at end of this session:** a baseline pass against the *current, unmodified* `1_workflow.xml` was about to begin — deliberately run before any Mode Writer fixes land, so we have a clean "before" data point for comparison once fixes are applied (particularly relevant to the new TC-3.2 wording, which tests for the sequencing rule in 3a above — that rule doesn't exist in the current XML yet, so TC-3.2 may legitimately fail on this baseline pass, which is expected and useful, not a surprise).

---

## 6. Pending Mode Writer Briefs (none sent yet — draft and send in next session)

In priority order as discussed:

1. **Sequencing rule** (Section 3a): tool's own execution-approval click must never substitute for `ask_followup_question` content review; the latter must complete with an explicit response before the tool call is attempted. High priority — likely root cause of Gate #1/#3 reliability issues.
2. **`custom_modes.yaml` sync reminder** (Section 2, item 7): standing checklist addition for every future brief, not a one-time fix.
3. **Existing-issue (`#N`) fix workflow** (Section 4, item 1): needs the assignment-logic decision resolved first.
4. **Feature/enhancement request template** (Section 4, item 2): lower priority, can be batched with #3.
5. **Gate option ordering for genuinely destructive actions** (Section 3a): not yet scoped — needs a judgment call on which action(s) qualify before this becomes a real brief. Do not send a blanket reordering brief.

**Reminder for whoever picks this up:** Mode Writer has no visibility into test IDs, the bug catalog, or this handoff doc — translate everything above into protocol-level prose before sending (e.g., "Enforce that Gate #1/#2/#3 approval must be obtained via an explicit follow-up question before any create/push/merge tool is invoked, and that a tool's own execution-approval prompt does not satisfy this requirement" — not "fix TC-3.2").
