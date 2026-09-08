# Next Steps

## Problems we were facing

We were facing a series of regressions and fixes that never seemed to work when testing the `GitHub Issue` mode. We did a number of tests, including looking into the specifics of how Zoo Code modes work, as well as their tool use.

### Test harness

We created a brand new `Test Harness` mode. This was so we could test things such as tool calls and hard gates without anything being lost in noise. During this phase, we had issues in which it appeared that the .xml system prompts of the test harness were never even being read.

## Root cause found

### Cause

After a series of tests, I discovered a major blunder on my part: Our repository edits have been writing to the wrong directory. The active runtime directory used by Zoo Code was relocated at some point to `C:\Users\Admin\.roo`, whereas our workspace edits and file modifications were landing in `C:\Users\Admin\AppData\Roaming\Code\User\globalStorage\zoocodeorganization.zoo-code`. Because of this path disconnect, recent test runs operated under mismatched or completely missing instruction file.

We found that `rules-github-issue` existed in two places: the `.roo` directory, and the (incorrect) `globalStorage` directory. The `.roo` directory was last modified 3 days prior to this discovery, and is likely the most stale; however we are uncertain which contains what.

### Implications

* **`test-harness` Mystery Solved:** The mode never existed in the active `.roo` directory. The model ran with **zero custom instructions** (only basic tool restrictions), explaining symptoms like invented to-do items, missing followup questions, and absent widget commands. The test-harness design was never genuinely tested.
* **`R1` Validity Under Review:** Because `.roo` rules haven't been updated in 3 days, `R1` (run Sept 7) tested an older protocol draft rather than the latest repo revisions. While observed behaviors (e.g., to-do item bundling causing same-turn skips) remain valid, any claim of the form *"the XML said X but the model did Y"* requires re-verification against the exact `.roo` draft used during `R1`.

### Your suggested next steps

1. **Verify Live Structure:** Confirm exact relative paths under `C:\Users\Admin\.roo\` for rules (e.g., `.roo\rules\rules-github-issue\...` vs. `.roo\rules-github-issue\...`) and determine if `custom_modes.yaml` lives in `.roo` or remains linked in `globalStorage`.
2. **Diff Before Overwriting:** Diff `.roo` rule files against current repo files to ensure no directly edited in-app changes are lost before aligning on the canonical version.
3. **Repoint Repo/Symlinks:** Re-anchor the working tree or hard symlinks to the verified `.roo` path.
4. **Run Canary Verification:** Insert an unmistakable throwaway marker (e.g., a unique comment) into the rule files at the new location to confirm the model loads it in a single quick trial before resuming real test matrix runs.
5. **Update Documentation:** Update `AGENTS.md` to reflect `C:\Users\Admin\.roo` as the true active directory to prevent future silent path mismatch failures.

### What I have done so far

1. **Live Structure:** There is no `/rules/` parent directory: The correct structure is `.roo\rules-github-issue\...`
2. **Diff Before Overwriting:** You will complete this step. The old, `.roo` .xml files exist in `oldrules-github-issue`, whereas the newer `globalStorage` files exist in `rules-github-issue`. We must see what if anything should be merged.
3. **Repoint Repo:** Complete.
4. **Run Canary Verification:** I added a step in the test harness telling the mode to ask if the user "wants to party." I ran an informal test and found this to work.
5. **Update Documentation:** I updated the one reference that I could see. If you see any other areas it needs to be updated, tell me.

## Once complete

Once we have merged the two `github-issue` directories, we have two directions we can go:

1. Continue doing tests using the test harness. If there are any open questions regarding the operattion of modes right now, or questions arise later, we now have this tool available to us.
2. Run the test_matrix against `GitHub Issues` mode again. We should start from scratch. Previous assumptions of what was or was not working are now invalid.

## Larger questions

We also discussed previously if we are taking the right approach, essentially creating a state machine. We discussed whether the mode's size is growing to large, and the model (Gemini 3.5 Flash Lite) was getting confused. We should run the tests again before we decide on this,  but it is worth considering.

The state machine question is one I specifically want to consider. If we can rework the mode to be more robust, and to make decisions on its own, it will be able to handle scenarios on its own, including those we have not explicitly defined, rather than falling into the "state machine trap."

### rules-mode-writer

You may have noticed that the repo now contains the `rules-mode-writer`. This is the `Mode Writer` node we have been handing off to. It was already in this directory, and I decided not to add it to `.gitignore`, at least temporarily. The reasoning being:

* We can use it to get a better understanding of how modes work, sinnce it spells out much of what goes into making a mode.
* We can use its own structure as a reference point for writing modes. Having a pre-built mode as a reference for how one might style a mode could be useful. For example, it defines its own .xml files that we do not use. This is instructive: We ccan design our own .xml structure, and do not need to follow the standard/default that we are now.

  If we desired, I could pull in other pre-built modes to see how they are written.  

* It may be useful when determining how to write the prompts we hand off to it.

## Debug mode logs

I am uncertain if this has been documented anywhere, but we also discovered where to find the Zoo Code logs. There are 3 available to us:

* Task History (markdown)
* API History (JSON)
* UI History (JSON)

You determined `task history` to be most useful, and it is what I will be sharing with you when we run tests, in place of the copy-paste of the trace that we were doing before.
