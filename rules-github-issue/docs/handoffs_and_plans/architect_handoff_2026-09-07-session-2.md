# Architect AI Handoff — ZooCode GitHub Issue Mode (Session 2, 2026-09-08)

**Purpose:** Carry-forward for next conversation. Picks up immediately after the 2026-09-07 handoff. Test matrix already updated by user with R1 — this doc covers everything *not* in that file.

---

## 1. Session Summary

Ran **R1**: first live test post the full protocol/matrix reset described in the 2026-09-07 handoff. Single continuous run, root invocation, full repo reset, BUG-1.1 (`config.py` port concatenation). Scored against the test matrix turn-by-turn as UI summaries came in, then re-verified against two raw debug logs (Task history markdown, UI history JSON) the user pulled from Zoo Code's debug export after the fact. **User already has the updated `test_matrix.md` with all R1 verdicts — not reproduced here.**

---

## 2. Fixed Project Constraint (not a variable to test around)

**Model is `gemini-flash-lite-latest` for all runs** — user's deliberate choice (500 free requests/day). Do not treat this as a confound to control for or suggest switching; design Mode Writer recommendations assuming this model's compliance ceiling, which R1 showed is low under complex multi-gate instructions. Practical implication: **favor structural/architectural enforcement over added prose instructions** wherever possible, since a lite model is exactly the profile most likely to skip steps under token/latency pressure no matter how clearly the XML states the rule.

---

## 3. R1 — What Actually Happened (root causes, corrected)

1. **Both Gate #1 and Gate #3 were skipped entirely.** The model drafted issue content / formulated the fix summary internally, then called `create_issue` / proceeded to commit+push+close in the same turn — **never invoking `ask_followup_question`** for content review beforehand. This is a pure model/prompt-compliance gap.
2. **IMPORTANT CORRECTION (user caught this):** Tool-execution auto-approval (the user's own client setting, approving individual tool calls like `create_issue`/git commands from firing without a manual click) is **unrelated** to Gate integrity and should not be cited as a cause. It's a legitimate, orthogonal workflow preference. The `ask_followup_question` calls themselves were never auto-approved and did wait for genuine human input (~11 min and ~9 min real gaps observed in timestamps) — proving the *ask* mechanism itself works fine when the model actually calls it. The failure is 100% that the model chose not to call it at the right points, not an artifact of the approval settings. **Do not reintroduce the "auto-approval defeats gates" framing in future analysis.**
3. **Mode-level tool restriction is real and structural** (resolves handoff Section 3a/3b's open question). Raw log shows `edit_file` rejected with `"Tool \"edit_file\" is not allowed in github-issue mode"` — this is an execution-layer block, independent of the XML prose. Good news: sub-mode isolation (TC-5.1) has a hard backstop, not just instructions. (Separately, `edit_file` was *also* rejected in Code mode for being the wrong tool name — the model recovered using `edit` instead — that's model confusion, not a governance signal.)
4. **Manual issue closure (TC-5.8) — most severe finding, timestamp-confirmed.** `update_issue(state=closed)` was called in the *same turn* as a banned `;`-chained git command, with zero dependency between them. The chained git command failed instantly; the issue closed successfully at **05:53:50**. The agent then retried git add/commit/push unchained, completing the actual push at **05:54:10** — **~20 seconds after the issue was already manually closed.** The closure had no dependency on the fix ever successfully reaching remote, let alone a PR existing. No PR was ever opened in this run.
5. Phase 1 identity/permission resolution (`user.email` lookup, `STAKEHOLDER_USERNAME`, `CAN_MERGE`) was skipped entirely — never attempted. This blocks any Phase 6 merge-gate verdicts (all scored BLOCKED, not FAIL).
6. Phase 6 (CAN_MERGE eval, merge gate, workspace restore, branch cleanup) was skipped wholesale; `attempt_completion` fired immediately after the manual close.

---

## 4. Log-Type Guidance for Future Runs

Three debug log types are available from Zoo Code's debug export: **Task history** (markdown), **API history** (JSON), **UI history** (JSON).

- **Default going forward: Task history only.** Complete — reasoning blocks, exact tool inputs/outputs, mode switches, verbatim gate text. Sufficient for scoring nearly every TC.
- **API history: skip by default.** Redundant with Task history's content, padded with large non-useful `thoughtSignature` blobs.
- **UI history: request only if a specific ambiguity needs resolving** (e.g., timestamp precision, `autoApprovalDecision` metadata). It's what let us catch and then correct the auto-approval point in this session, but it's not needed every run now that the mechanism is understood.
- **User's stated preference:** paste log(s) once at the **end** of a run, not throughout, to save tokens. Architect should ask for only what's needed for the specific TCs in question.

---

## 5. Pending Mode Writer Briefs (none sent yet — still all pending from the 2026-09-07 handoff, now with stronger R1 evidence to cite)

Priority order, updated with R1 findings:

1. **Sequencing rule (highest priority, now empirically confirmed twice by R1):** Enforce that Gate #1/#2/#3 approval must be obtained via an explicit follow-up question, with an explicit human response, *before* any create/commit/push/merge/close tool is invoked — and that this must hold even under a low-compliance model. Frame as a hard sequencing requirement, not a suggestion.
2. **NEW, elevated to high priority by R1:** Explicit rule that **issue closure must never be attempted except via native PR-merge webhook**, and that this is independent of whether the fix was ever pushed successfully. R1 showed the model will manually close an issue with zero regard for whether the underlying code change succeeded — this needs to be stated as absolute, not contingent on "after PR merge."
3. **`custom_modes.yaml` sync reminder** — standing checklist item for every future brief (per 2026-09-07 handoff item 7).
4. **Existing-issue (`#N`) fix workflow** — needs the assignment-logic decision resolved first (per 2026-09-07 handoff).
5. **Feature/enhancement request template** — lower priority, batch with #4.
6. **Gate option ordering for genuinely destructive actions** — still not scoped, needs judgment call on which action(s) qualify; do not send a blanket reordering brief (per 2026-09-07 handoff — this ruling stands unchanged).

**Reminder:** Mode Writer has no visibility into test IDs, bug catalog, or handoff docs — translate everything above into protocol-level prose before sending.

---

## 6. Open Items / Next Steps

- Test matrix already updated with R1 verdicts by user — pick up from there.
- No Mode Writer briefs sent yet this session either — still all pending.
- Repo state after R1: `Unchanged from prior run` (issue #1 closed, branch `issue-1-fix-db-port` on origin unmerged/undeleted, `config.py` fixed). Decide reset strategy before R2.
- Consider whether next run should target Phase 2 duplicate-handling (TC-2.2/2.7) by reusing the dirty state, or reset for a clean signal — this was under discussion when the debug logs interrupted the flow (see prior turn for the BUG-1.2-no-reset rationale, still valid if useful).