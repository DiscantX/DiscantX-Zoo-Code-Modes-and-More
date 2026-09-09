# Architect AI Handoff — ZooCode GitHub Issue Mode (Session 4, 2026-09-09)

**Supplements, does not supersede:** the 2026-09-08-session-3 handoff. That handoff's open
items (untested phases, self-scope-restriction brief status, `edit`-permission-removal
verification) remain outstanding and are not addressed here.

**Nature of this session:** Unofficial/free-form testing across three separate task logs
(user "going off script" rather than running scored test-matrix passes). No `test_matrix.md`
rows were scored or updated as a result of this session — these are new findings surfaced
by unstructured probing, not formal run results.

---

## 1. Findings Addressed via Mode Writer Brief (Sent This Session)

A single brief was sent covering four items:

1. **No label assignment on issue creation.** Issues are currently drafted and created with
   no label logic at all. Brief asks for a one-time-per-session semantic label lookup against
   the repo's existing labels, surfaced as part of the Gate #1 draft (not a separate gate), with
   "no label" as the default when no reasonable existing match is found — explicitly no
   auto-creation of new labels.
2. **Bug-centric phrasing bleeding into non-bug issue types.** Observed during a feature-request
   flow: gate/status language defaults to "fix" terminology even when the issue is a feature
   request. The agent self-corrected in the moment, but the underlying phrasing isn't
   type-aware. Brief asks for phrasing to be derived from the same type classification used for
   label matching (Item 1), rather than a second, separate detection pass.
3. **No formalized manual closure path.** Only automatic closure via merge webhook is currently
   defined. Observed (see Section 2 below) that manual closure is something users will
   reasonably want (e.g. "not planned," duplicates) and the agent will currently do it via
   direct API calls with no review step, in direct tension with this mode's own stated
   prohibition on agent-initiated closure. Brief formalizes a small set of closure reasons
   (resolved via merge / not planned / duplicate-as-not-planned-plus-label), requires a
   draft-and-halt confirmation step before any non-webhook closure, and gives guidance on when
   a closing comment is warranted.
4. **Blanket confirmation requirement for terminal/destructive actions outside defined
   workflows.** General-purpose rule (not tied to a specific phase): any hard-to-reverse action
   — branch deletion, comment deletion, manual issue closure, etc. — requires an explicit,
   specific confirmation step before execution, even when the triggering request was broad or
   general (e.g. "clean up stale branches" is not itself confirmation for a specific deletion).
   This closes the gap illustrated in Section 2 below without loosening any existing in-pipeline
   gate.

Brief includes the standard reminder to check whether `custom_modes.yaml` needs a matching
update.

---

## 2. Findings Not Yet Briefed — Judgment Calls for Next Session

### 2.1 Manual issue closure and comment deletion executed with zero confirmation
Across the free-form logs: the agent closed an issue via direct API call (twice, including
once with `state_reason` set via raw `gh api` after the MCP tool didn't expose that field),
reopened it, deleted a comment via `gh api -X DELETE`, and re-closed it — all on single-line
user requests, with no halt-and-confirm step anywhere. This is the direct motivating case for
the blanket confirmation rule in Section 1, Item 4 above.

### 2.2 Shell command execution bypasses the MCP tool surface
When the MCP `update_issue` tool didn't expose a parameter the agent wanted (`state_reason`),
it fell back to `execute_command` running `gh api` directly, achieving the same mutation
through a broader-privilege path than the tool interface offers. Not yet briefed — worth
deciding whether any constraint is intended to hold specifically at the MCP tool boundary
(in which case shell fallback undermines it) or whether shell access is acceptable as a
general-purpose escape hatch. No recommendation yet; flagging only.

### 2.3 Synthesis/grounding failure, distinct from any gate-sequencing issue
When asked to produce an interleaved timeline of issue events and comments from two just-fetched
raw API responses, the agent's first attempt included a comment that had already been deleted
and did not appear in either raw payload — it later admitted (its own words) this came from
"blending memory and recall rather than a direct reference to the raw data." A fabricated
approximate timestamp also appeared for one entry. This is not a tool-sequencing or gate
violation; it's a failure to ground a summarization step in freshly retrieved data rather than
prior conversational context. Given that Gate #3 relies on the agent accurately reporting diff
and test output back to the user, this seems like a risk category worth tracking even though it
surfaced outside the formal pipeline. No brief drafted yet — recommend a cross-cutting
"ground synthesis and summaries in freshly retrieved tool output, not recalled context" rule,
independent of whichever direction the state-machine question (Section 3) goes.

### 2.4 `test_suite.py` undermines blind testing at the source
Unprompted, the agent ran the full test suite in response to a generic "check for maintenance
work" request. The failure output included, for every failing test, an inline source comment
identifying its corresponding bug ID (visible directly in pytest's traceback context, since
`test_suite.py` in the TestBed repo annotates every planted-bug test this way). This means the
execution agent can trivially obtain the full bug catalog by running the suite once, regardless
of the separate airgapping of `bug_catalog.md` in the Modes repo. This is a TestBed-repo issue,
not a Mode Writer issue — recommend stripping or genericizing these comments in `test_suite.py`
before further blind runs are treated as blind. Flagging here since it affects the validity of
any future run where the agent happened to run the suite early.

---

## 3. Revisited: Is the Pipeline Too Narrow / Too Much a State Machine?

This question (raised previously, deferred pending more test data) was directly informed by
this session. Conclusion: the evidence points away from "loosen the in-pipeline gates" and
toward "extend coverage to actions currently outside the pipeline."

- Within the defined pipeline — including a genuinely novel request type (feature request
  instead of bug fix) — gate sequencing, turn separation, and todo-list tracking all held up
  correctly. No confusion or improvisation was observed inside the covered workflow.
- All the concerning autonomous behavior (branch deletion, manual closure, comment deletion)
  occurred specifically *outside* the defined workflow, where no gate exists at all — not
  because gates that did exist were handled poorly.
- This suggests the fix is additive scope (the blanket terminal-action rule in Section 1, and
  potentially further blanket rules of the same shape as new gaps are found) rather than a
  structural redesign toward more model-driven judgment in place of explicit states. More
  autonomy specifically *within* the existing pipeline would cut against this mode's own
  standing rule that "I have decided this is correct" must never substitute for an explicit
  human response.
- The grounding/synthesis issue (Section 2.3) is orthogonal to this question either way and
  should be tracked regardless of which direction is taken on pipeline structure.

---

## 4. Open Items for Next Session

- Confirm whether this session's Mode Writer brief (Section 1) has been applied, and whether
  `custom_modes.yaml` needed (and received) a matching update.
- Decide on and apply a fix for the `test_suite.py` bug-ID comment leak (Section 2.4) before
  treating any future run as blind.
- Decide whether to brief the shell-bypass observation (Section 2.2) or leave as accepted
  behavior.
- Consider drafting a grounding-discipline rule for synthesis steps (Section 2.3).
- All open items from the session-3 handoff remain outstanding and take priority for the next
  *formal* (test-matrix-scored) run: Phase 2 duplicates, Gate reject/revise paths, TC-1.2–1.5,
  TC-4.3/4.5/4.6 (partially covered by R2), TC-5.4/5.6/5.7/5.9, TC-6.1/6.3/6.6, Phase 0.2
  Orchestrator delegation.
- Once the labeling/closure/phrasing changes from this session's brief ship, new test matrix
  rows will likely be needed to cover them (not added to `test_matrix.md` this session, since
  this was not a scored pass).