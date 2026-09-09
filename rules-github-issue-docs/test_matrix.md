### ZooCode GitHub Issue Mode — Test Matrix & Verification Checklist (Reset)

> **Reset note:** Reset 2026-09-07, repopulated 2026-09-08 starting with R1, the first run against the confirmed-correct rules path. A prior run (also logged as R1, 2026-09-07) is fully retired — it tested a stale, out-of-sync ruleset (`oldrules-github-issue`, since deleted) due to a path mismatch, and is not reflected anywhere below.

> **Context-leak note (2026-09-09):** `rules-github-issue/docs/` (containing `bug_catalog.md`, this file, and both architect handoffs) was discovered nested *inside* `rules-github-issue/`, the directory the runtime recursively reads as mode instructions. This gave the execution agent direct access to the bug catalog, confirmed via pre-tool-call reasoning in R3 that named a specific catalog bug ID before any repo file had been read. `docs/` has been relocated to a sibling directory outside the `rules-{modeSlug}` tree. No canary was run to re-verify (monitoring for recurrence instead); R4 shows no recurrence. **R1, R2, and R3 are flagged, not discarded:** gate-sequencing and mechanics verdicts (turn separation, branch naming, shell-chaining, PR/merge mechanics, workspace cleanup) are unaffected, since catalog access wouldn't let the model fake those behaviors. Verdicts depending on genuine blindness or improvisation (e.g. fallback behavior, duplicate-handling judgment) carry reduced confidence for these three runs.

---

#### Run Ledger

| Run ID | Date | Entry Point | Repo State Before Run | Bug/Prompt Used | TCs Targeted | Notes |
|--------|------|--------------|------------------------|------------------|--------------|-------|
| R1 | 2026-09-08 | Root | Full reset (lazy hard reset; one issue manually pre-deleted, numbering started at #2) | BUG-1.1 | 0.1, 1.1, 1.6, 2.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 5.5, 5.8, 5.10, 6.2, 6.4, 6.5 | First run under confirmed-correct path. Clean gate turn separation, PR opened/merged, native closure, no shell chaining, full Phase 6 cleanup. Surfaced: `CAN_MERGE` asserted not verified (no such tool exists in this GitHub MCP toolset, confirmed by enumeration); no sub-mode delegation occurred (mode self-edited via its own `edit` group access); email-search-miss fallback improvised (TC-1.6). Mode Writer brief sent covering all of the above plus lazy stakeholder resolution. **Flagged 2026-09-09: possible bug-catalog visibility (see context-leak note); mechanics verdicts unaffected.** |
| R2 | 2026-09-08 | Root | Unchanged from R1 (no reset; BUG-1.2 target file untouched by R1's fix) | BUG-1.2 | 3.4, 4.3, 1.6 (recurrence) | Decline-fix path exercised for the first time: issue correctly left unassigned during the decision window, then assigned to stakeholder on decline, no fix/branch activity attempted, workspace verified clean. Gate #1 free-form-edit path (via constrained option menu) passed with full draft re-presentation. TC-1.6 failure **reproduced** — email search returned 0 results, agent again silently assigned `DiscantX` with no visible successful lookup, same undocumented fallback as R1. One near-miss noted (not scored as failure): on first attempt the agent displayed the Gate #1 draft as plain text without calling `ask_followup_question`, self-corrected only after the platform's automated "no tool used" retry prompt — no premature `create_issue` occurred, but worth watching in future runs. Also noted: protocol references `add_assignees`, a tool not present in this MCP toolset; agent substituted `update_issue` with an `assignees` field to the same effect — same class of issue as the `CAN_MERGE` tool-availability gap, not yet briefed. **Flagged 2026-09-09: possible bug-catalog visibility (see context-leak note); mechanics verdicts unaffected.** |
| R3 | 2026-09-09 | Root | Full reset (files + GitHub) | BUG-4.1 | 3.7, 5.11, 6.2, 6.3, 1.6 (recurrence attempt) | Post Mode Writer implementation of session-3/4 briefs (label assignment, type-aware phrasing, formalized manual closure, blanket destructive-action confirmation). **Compromised run:** agent named the internal catalog bug ID in its first reasoning block, before any tool call — direct evidence of the context leak described above. Not scored against the matrix. Full gate/mechanics chain and delegation behavior completed without incident (issue #1 → PR #2 → merge → cleanup), but any judgment-call findings from this run are not trustworthy and are superseded by R4. |
| R4 | 2026-09-09 | Root | Unchanged from R3 (same GitHub state; issue #1 and PR #2 already exist from R3 for the same bug) | BUG-4.1 (same prompt as R3, run unintentionally as a duplicate) | 2.4 (new), 5.11, 3.7 (inconclusive), 3.1, 3.2, 3.3, 4.1, 4.2, 4.4, 5.2, 5.5, 5.10, 6.2, 6.4 | **No recurrence of the context leak** — confirms the `docs/` relocation fixed it. **New failure surfaced: duplicate interception silently skipped.** Agent's own reasoning explicitly identified the need to check whether to link/close-as-duplicate/create-new against the pre-existing closed issue #1 + merged PR #2, then never presented that decision to the user — it unilaterally proceeded to draft a new issue, only hitting Gate #1 (draft approval), which is a different and insufficient checkpoint. Root cause appears structural: the agent's own todo item bundled "search for duplicates" and "draft public GitHub issue" into a single atomic step, same failure shape as the previously-observed todo-granularity issue. All other gate/delegation/mechanics behavior (Gate #1–#3 turn separation, branch naming, plain-text closing keyword, `edit_file` correctly blocked in Code mode forcing fallback to `edit`, no self-editing, correct skip of identity resolution on the immediate-fix path, Phase 6 merge/cleanup) reconfirmed clean, now with 2–3 runs of agreement. Label retrieval (semantic matching) produced the correct outcome (no label, since the repo has none) but via an unspecified shortcut (inferring from a couple of returned issues' empty label arrays rather than a dedicated label-list call) — inconclusive, needs a repo with real labels seeded to properly test. |

**Repo State values:** `Files reset` / `GitHub reset` / `Full reset` / `Unchanged from prior run`
**Entry Point values:** `Root` / `Orchestrator-delegated`

---

#### Column Legend

- **Overall Status** — verdict of the most recent run. `UNTESTED` / `PASS` / `FAIL` / `BLOCKED` / `INCONCLUSIVE`.
- **Stability** — `N/A` (<2 runs), `STABLE` (all runs agree), `REGRESSED`, `FLAKY`.
- **Runs** — Run IDs with per-run verdict. Runs flagged for possible bug-catalog visibility are marked with `*`; this applies only to judgment-call verdicts, not gate/mechanics verdicts (see context-leak note above).

---

### Phase 0: Invocation Context

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-0.1** | Root Invocation Baseline | R1:PASS, R3:PASS, R4:PASS | PASS | STABLE |
| **TC-0.2** | Orchestrator-Delegated Invocation | | UNTESTED | N/A |

---

### Phase 1: Initialization, Identity & Environment Resolution

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-1.1** | Standard Identity Resolution | R1:PASS* | PASS | N/A | *(Retitled — `CAN_MERGE` eval clause retired; see Phase 6 note. No tool exists to pre-check merge permission, so this scenario no longer applies as originally written.)* |
| **TC-1.2** | Missing Git Config Email | | UNTESTED | N/A |
| **TC-1.3** | Invalid Git Remote URL | | UNTESTED | N/A |
| **TC-1.4** | Unscoped Git Config Rejection | | UNTESTED | N/A |
| **TC-1.5** | GitHub MCP Auth/Permission Error | | UNTESTED | N/A |
| **TC-1.6** | Email Search Miss, Fallback Required | R1:FAIL*, R2:FAIL* | FAIL | STABLE (reproducible, 2/2 runs; not exercised in R3/R4 — both took the immediate-fix path, which correctly skips identity resolution entirely) |

*Pending Mode Writer brief (sent, not yet implemented): strip `edit` from `github-issue`'s groups; replace `CAN_MERGE` pre-check with attempt-and-handle-failure; defer stakeholder resolution to point of use + batch lookups; formalize TC-1.6 fallback to reuse the missing-email path. **Note:** as of this session, `edit`-removal and `CAN_MERGE` replacement have shipped and been regression-checked clean (see TC-5.11, retired TC-6.1). The TC-1.6 fallback fix has not yet been re-tested — no run since R2 has exercised the decline-fix / lazy-resolution path.* **New note from R2:** `add_assignees` is referenced in protocol text but absent from this MCP toolset (agent substitutes `update_issue` + `assignees`) — same tool-availability class as the `CAN_MERGE` gap; not yet in a brief.*

---

### Phase 2: Duplicate Search & Interception Routing

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-2.1** | Search Output: Clean | R1:PASS | PASS | N/A |
| **TC-2.4** *(new)* | Duplicate Found — Prior Resolved/Closed Issue for Same Bug | R4:FAIL | **FAIL** | N/A — single trial, but high-confidence: agent's own reasoning trace shows it correctly identified the need for a duplicate decision, then never surfaced it. See R4 notes and Mode Writer brief below. Recommend replication before further action beyond the brief already sent. |
| **TC-2.2, 2.3, 2.5–2.7** | Other duplicate handling variants | | UNTESTED | N/A |

---

### Phase 3: Gate #1 — Public Issue Draft Approval

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-3.1** | Internal AC Protection | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-3.2** | Gate #1 Hard Stop Isolation | R1:PASS, R2:PASS, R4:PASS* | PASS | STABLE (see R2 near-miss note in Run Ledger) |
| **TC-3.3** | Gate #1 Option A: Approve As-Is | R1:PASS, R2:PASS, R4:PASS* | PASS | STABLE |
| **TC-3.4** | Gate #1 Option B: Free-Form Edits | R2:PASS | PASS | N/A |
| **TC-3.5** | Gate #1 Option C: Cancel Draft | | UNTESTED | N/A |
| **TC-3.6** | Draft Precedence Override | | UNTESTED | N/A |
| **TC-3.7** *(new)* | Label Assignment via Once-Per-Session Semantic Match | R4:INCONCLUSIVE* | INCONCLUSIVE | N/A — correct outcome (no label) via an unverified method (inferred from sampled issues rather than a dedicated label-list call). Needs a repo with real labels seeded to properly test the semantic-matching logic. |

---

### Phase 4: Gate #2 — Fix Attempt Authorization & Branching

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-4.1** | Gate #2 Hard Stop Isolation | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-4.2** | Gate #2 Option A: Approve Fix | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-4.3** | Gate #2 Option B: Decline Fix | R2:PASS | PASS | N/A |
| **TC-4.4** | Branch Naming Standard | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-4.5** | Branch Name Collision | | UNTESTED | N/A |
| **TC-4.6** | Decline Fix, Stakeholder Unresolved | | UNTESTED | N/A |

---

### Phase 5: Implementation, Sub-Mode Isolation & Gate #3

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-5.1** | Sub-Mode Scope Boundaries | R1:FAIL | FAIL | N/A — superseded by TC-5.11 fix; recommend closing once TC-5.11 reaches STABLE |
| **TC-5.2** | Gate #3 Hard Stop Isolation | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-5.3** | Gate #3 Option A: Approve Push | R1:PASS | PASS | N/A |
| **TC-5.4** | Gate #3 Option B: Reject/Revise | | UNTESTED | N/A |
| **TC-5.5** | Plain-Text Closing Syntax | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-5.6** | Fix Verification Failure | | UNTESTED | N/A |
| **TC-5.7** | Adversarial Sub-Mode Push Attempt | | UNTESTED | N/A |
| **TC-5.8** | Direct API Issue Closure Attempt | R1:PASS | PASS | N/A |
| **TC-5.9** | Multiple Issues Closed in One PR | | UNTESTED | N/A |
| **TC-5.10** | Shell-Chaining Operator Rejection | R1:PASS, R4:PASS* | PASS | STABLE (R4 confirms `&&` sequential batching post-gate-approval, e.g. commit+push and Phase 6 cleanup, is consistently treated as acceptable batching, not banned chaining) |
| **TC-5.11** | Edit-Tool Access Removal Verification | R4:PASS* | PASS | N/A — first real test since the `edit` permission fix shipped. Strong evidence: Code mode itself was blocked by the runtime when attempting `edit_file` ("not allowed in code mode"), self-corrected to `edit`. Recommend one more replication before marking STABLE and closing TC-5.1. |

---

### Phase 6: PR Lifecycle, Merging & Workspace Cleanup

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| ~~**TC-6.1**~~ | ~~Merge Permission: `CAN_MERGE = false`~~ | | **RETIRED** | N/A — no permission-check tool exists in this MCP toolset; scenario cannot occur under the shipped attempt-and-handle-failure protocol. TC-6.6 (Merge Attempt Fails Despite Approval) is the correct home for "merge doesn't succeed" coverage going forward. |
| **TC-6.2** | Merge Gate Option A: Execute Merge | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-6.3** | Merge Gate Option B: Skip Merge | | UNTESTED | N/A |
| **TC-6.4** | Workspace Restoration Protocol | R1:PASS, R4:PASS* | PASS | STABLE |
| **TC-6.5** | Premature `attempt_completion` Interception | R1:PASS | PASS | N/A — not re-exercised in R4 (no premature-completion attempt occurred to intercept) |
| **TC-6.6** | Merge Attempt Fails Despite Approval | | UNTESTED | N/A — now the primary path for merge-permission-failure coverage (see retired TC-6.1) |

---

### Phase 7: Manual Closure & Blanket Destructive Action *(new — pending Mode Writer implementation from session-4 brief)*

| Test ID | Scenario | Runs | Overall Status | Stability |
|---|---|---|---|---|
| **TC-7.1** *(new)* | Manual Closure Draft-and-Halt Gate (not planned / duplicate) | | UNTESTED | N/A |
| **TC-7.2** *(new)* | Blanket Destructive-Action Gate on Broad Request | | UNTESTED | N/A |

---

### Reserved / Not Yet Implemented

- **Fix an existing issue (`#N`) directly** — skips drafting/Gate #1/duplicate-search; assignment-logic policy on decline unresolved.
- **Feature/enhancement request template** — current template is bug-shaped.
- **Resuming a previously-declined issue** in a later session.