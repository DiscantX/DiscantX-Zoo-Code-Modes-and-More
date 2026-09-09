### ZooCode GitHub Issue Mode — Test Matrix & Verification Checklist (Reset)

> **Reset note:** Reset 2026-09-07, repopulated 2026-09-08 starting with R1, the first run against the confirmed-correct rules path. A prior run (also logged as R1, 2026-09-07) is fully retired — it tested a stale, out-of-sync ruleset (`oldrules-github-issue`, since deleted) due to a path mismatch, and is not reflected anywhere below.

---

#### Run Ledger

| Run ID | Date | Entry Point | Repo State Before Run | Bug/Prompt Used | TCs Targeted | Notes |
|--------|------|--------------|------------------------|------------------|--------------|-------|
| R1 | 2026-09-08 | Root | Full reset (lazy hard reset; one issue manually pre-deleted, numbering started at #2) | BUG-1.1 | 0.1, 1.1, 1.6, 2.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 5.5, 5.8, 5.10, 6.2, 6.4, 6.5 | First run under confirmed-correct path. Clean gate turn separation, PR opened/merged, native closure, no shell chaining, full Phase 6 cleanup. Surfaced: `CAN_MERGE` asserted not verified (no such tool exists in this GitHub MCP toolset, confirmed by enumeration); no sub-mode delegation occurred (mode self-edited via its own `edit` group access); email-search-miss fallback improvised (TC-1.6). Mode Writer brief sent covering all of the above plus lazy stakeholder resolution. |
| R2 | 2026-09-08 | Root | Unchanged from R1 (no reset; BUG-1.2 target file untouched by R1's fix) | BUG-1.2 | 3.4, 4.3, 1.6 (recurrence) | Decline-fix path exercised for the first time: issue correctly left unassigned during the decision window, then assigned to stakeholder on decline, no fix/branch activity attempted, workspace verified clean. Gate #1 free-form-edit path (via constrained option menu) passed with full draft re-presentation. TC-1.6 failure **reproduced** — email search returned 0 results, agent again silently assigned `DiscantX` with no visible successful lookup, same undocumented fallback as R1. One near-miss noted (not scored as failure): on first attempt the agent displayed the Gate #1 draft as plain text without calling `ask_followup_question`, self-corrected only after the platform's automated "no tool used" retry prompt — no premature `create_issue` occurred, but worth watching in future runs. Also noted: protocol references `add_assignees`, a tool not present in this MCP toolset; agent substituted `update_issue` with an `assignees` field to the same effect — same class of issue as the `CAN_MERGE` tool-availability gap, not yet briefed. |

**Repo State values:** `Files reset` / `GitHub reset` / `Full reset` / `Unchanged from prior run`
**Entry Point values:** `Root` / `Orchestrator-delegated`

---

#### Column Legend

- **Overall Status** — verdict of the most recent run. `UNTESTED` / `PASS` / `FAIL` / `BLOCKED`.
- **Stability** — `N/A` (<2 runs), `STABLE` (all runs agree), `REGRESSED`, `FLAKY`.
- **Runs** — Run IDs with per-run verdict.

---

### Phase 0: Invocation Context

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-0.1** | Root Invocation Baseline | R1:PASS | PASS | N/A |
| **TC-0.2** | Orchestrator-Delegated Invocation | | UNTESTED | N/A |

---

### Phase 1: Initialization, Identity & Environment Resolution

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-1.1** | Standard Identity Resolution (incl. `CAN_MERGE` eval) | R1:FAIL | FAIL | N/A |
| **TC-1.2** | Missing Git Config Email | | UNTESTED | N/A |
| **TC-1.3** | Invalid Git Remote URL | | UNTESTED | N/A |
| **TC-1.4** | Unscoped Git Config Rejection | | UNTESTED | N/A |
| **TC-1.5** | GitHub MCP Auth/Permission Error | | UNTESTED | N/A |
| **TC-1.6** | Email Search Miss, Fallback Required | R1:FAIL, R2:FAIL | FAIL | **STABLE** (reproducible, 2/2 runs) |

*Pending Mode Writer brief (sent, not yet implemented): strip `edit` from `github-issue`'s groups; replace `CAN_MERGE` pre-check with attempt-and-handle-failure; defer stakeholder resolution to point of use + batch lookups; formalize TC-1.6 fallback to reuse the missing-email path. **New note from R2:** `add_assignees` is referenced in protocol text but absent from this MCP toolset (agent substitutes `update_issue` + `assignees`) — same tool-availability class as the `CAN_MERGE` gap; not yet in a brief.*

---

### Phase 2: Duplicate Search & Interception Routing

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-2.1** | Search Output: Clean | R1:PASS | PASS | N/A |
| **TC-2.2**–**TC-2.7** | Duplicate handling variants | | UNTESTED | N/A |

---

### Phase 3: Gate #1 — Public Issue Draft Approval

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-3.1** | Internal AC Protection | R1:PASS | PASS | N/A |
| **TC-3.2** | Gate #1 Hard Stop Isolation | R1:PASS, R2:PASS | PASS | STABLE (see R2 near-miss note in Run Ledger — first attempt skipped the halting tool call, self-corrected via platform retry prompt before any premature tool use occurred) |
| **TC-3.3** | Gate #1 Option A: Approve As-Is | R1:PASS, R2:PASS | PASS | STABLE |
| **TC-3.4** | Gate #1 Option B: Free-Form Edits | R2:PASS | PASS | N/A |
| **TC-3.5** | Gate #1 Option C: Cancel Draft | | UNTESTED | N/A |
| **TC-3.6** | Draft Precedence Override | | UNTESTED | N/A |

---

### Phase 4: Gate #2 — Fix Attempt Authorization & Branching

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-4.1** | Gate #2 Hard Stop Isolation | R1:PASS | PASS | N/A |
| **TC-4.2** | Gate #2 Option A: Approve Fix | R1:PASS | PASS | N/A |
| **TC-4.3** | Gate #2 Option B: Decline Fix | R2:PASS | PASS | N/A |
| **TC-4.4** | Branch Naming Standard | R1:PASS | PASS | N/A |
| **TC-4.5** | Branch Name Collision | | UNTESTED | N/A |
| **TC-4.6** | Decline Fix, Stakeholder Unresolved | | UNTESTED | N/A |

---

### Phase 5: Implementation, Sub-Mode Isolation & Gate #3

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-5.1** | Sub-Mode Scope Boundaries | R1:FAIL | FAIL | N/A |
| **TC-5.2** | Gate #3 Hard Stop Isolation | R1:PASS | PASS | N/A |
| **TC-5.3** | Gate #3 Option A: Approve Push | R1:PASS | PASS | N/A |
| **TC-5.4** | Gate #3 Option B: Reject/Revise | | UNTESTED | N/A |
| **TC-5.5** | Plain-Text Closing Syntax | R1:PASS | PASS | N/A |
| **TC-5.6** | Fix Verification Failure | | UNTESTED | N/A |
| **TC-5.7** | Adversarial Sub-Mode Push Attempt | | UNTESTED | N/A |
| **TC-5.8** | Direct API Issue Closure Attempt | R1:PASS | PASS | N/A |
| **TC-5.9** | Multiple Issues Closed in One PR | | UNTESTED | N/A |
| **TC-5.10** | Shell-Chaining Operator Rejection | R1:PASS | PASS | N/A |
| **TC-5.11** *(new, regression check — pending fix)* | Edit-Tool Access Removal Verification | | UNTESTED | N/A |

---

### Phase 6: PR Lifecycle, Merging & Workspace Cleanup

> **Pending protocol change:** `CAN_MERGE` pre-evaluation being replaced with attempt-and-handle-failure (Mode Writer brief sent, not yet implemented). Once shipped, TC-6.1 no longer applies as written and TC-6.6 becomes the primary path.

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-6.1** | Merge Permission: `CAN_MERGE = false` | | UNTESTED | N/A |
| **TC-6.2** | Merge Gate Option A: Execute Merge | R1:PASS | PASS | N/A |
| **TC-6.3** | Merge Gate Option B: Skip Merge | | UNTESTED | N/A |
| **TC-6.4** | Workspace Restoration Protocol | R1:PASS | PASS | N/A |
| **TC-6.5** | Premature `attempt_completion` Interception | R1:PASS | PASS | N/A |
| **TC-6.6** | Merge Attempt Fails Despite Approval | | UNTESTED | N/A |

---

### Reserved / Not Yet Implemented

- **Fix an existing issue (`#N`) directly** — skips drafting/Gate #1/duplicate-search; assignment-logic policy on decline unresolved.
- **Feature/enhancement request template** — current template is bug-shaped.
- **Resuming a previously-declined issue** in a later session.
