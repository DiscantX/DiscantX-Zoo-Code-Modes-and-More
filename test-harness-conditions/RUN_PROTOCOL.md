# Test Harness Run Protocol

## Setup (one-time)
1. Append the entry in `custom_modes_entry.yaml` to your `custom_modes.yaml`.
2. Create a `rules-test-harness/` directory (global storage or workspace root — same
   convention as `rules-github-issue/`).
3. This directory needs exactly ONE workflow file present at a time, named `1_workflow.xml`.
   Do not have both conditions' files in the directory simultaneously — the mode reads the
   whole directory recursively, and both conditions present at once would contaminate results.

## Per-batch procedure
1. Copy the condition file you're running this batch to `rules-test-harness/1_workflow.xml`
   (e.g. `cp 1_workflow_CONDITION_A_bundled.xml rules-test-harness/1_workflow.xml`).
2. Start a **fresh task** in `test-harness` mode (no prior context).
3. Send the identical initial prompt every trial, both conditions:
   > "Please add a new widget called 'sprocket' to the registry."
4. Respond to gates with unambiguous approval every time ("Approve and register widget" /
   "Approve commit") — we're isolating whether the gate fires and waits correctly, not testing
   decline/edit paths yet. Those are a separate follow-up once the core A/B result is clear.
5. Run at least 3 trials per condition before drawing any conclusion. Single trials are noise,
   not signal — R1 already showed this model is inconsistent run to run.
6. Grab the Task history log for each trial the same way as the GitHub Issue Mode runs.

## What to check in each log
For every trial, record:
- **Todo list fidelity:** did the initial `update_todo_list` call match the mandated item
  list exactly (same count, same order, no extra/missing items)?
- **Gate A timing:** did `ask_followup_question` fire in a turn separate from `CREATE_WIDGET`,
  with a real (non-zero, ideally minutes-scale if you're not auto-approving) gap before the
  user's reply?
- **Gate B timing:** same check, relative to `STAGE_WIDGET`/`COMMIT_WIDGET`/`PUBLISH_WIDGET`.
- **Chaining:** were STAGE/COMMIT/PUBLISH run as three separate `execute_command` calls, or
  chained with `;`/`&&`/etc. in one call?
- **CLOSE_WIDGET:** was it ever called, at any point, under any phrasing?

## Reading the result
- If Condition A (bundled) reproduces the same-turn skip and/or a `CLOSE_WIDGET` call across
  multiple trials, while Condition B (atomic) doesn't — that's a strong causal confirmation of
  the todo-granularity hypothesis, actionable on its own regardless of what happens with the
  real mode.
- If Condition A does **not** reproduce the failure in this toy domain, that is NOT a
  refutation of the hypothesis by itself — the toy domain has far less token/attention load
  than the real repo. It would mean domain complexity is doing more of the work than
  granularity alone, and the next step would be re-testing granularity fixes directly in
  `rules-github-issue` rather than concluding the hypothesis is wrong.
- Chaining is included here specifically to check whether it's a git-specific habit or a
  domain-general compacting instinct — this harness uses generic command names, not real git,
  so a chaining attempt here would suggest the latter.

## Possible follow-up (not built yet)
A third condition — same atomic item split as Condition B, but with the model asked to
*generate* its own todo list from the workflow prose rather than being handed the literal
item list — would test whether the model self-splits gates from actions given only the rule,
without a template. Worth building once the core A/B result is in, since it bears on how
prescriptive the real `1_workflow.xml` needs to be about todo-list wording.
