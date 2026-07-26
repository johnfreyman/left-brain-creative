# Third Path — Blind Quality Comparison (Trim vs Revert)

Follow-up to `EXEMPLAR-TEST-REPORT.md`. 10 situations (8 fresh, 2 carryover) × 3 generations × 2 arms = 60 cards, paired into 30 blind comparisons, judged by a fresh `claude-opus-4-8` call per pair (rubric: speakability, specificity, tightness, honesty of the hard part). Raw data in `quality-runs/`.

## Verdict: **REVERT**

Not the number the raw pass produced. Read the full reasoning below before treating this as a clean call either way — the corrected data supports a real but unresolved signal, and the report says so rather than picking whichever threshold looks cleanest.

## What happened, in order

**First pass:** 30 pairs, arm A won 21 (70.0%), arm B won 9, zero ties. Against the pre-registered rule (>60% → TRIM), this triggers TRIM.

**But the position-bias check (required before reporting) failed badly.** Card 1 won only 8/30 (26.7%); Card 2 won 22/30 (73.3%) — regardless of which arm occupied which slot. Crosstabbing arm against position made the confound obvious:

| | A wins | B wins |
|---|---|---|
| When A is Card 1 (n=15) | 7 | 8 |
| When A is Card 2 (n=15) | 14 | 1 |

When arm A sits in the disadvantaged position, it's a coin flip. When it sits in the advantaged position, it sweeps. The raw 70% figure is overwhelmingly a position artifact, not a content-quality signal. Per the pre-registered contingency, all 30 pairs were re-judged with positions flipped before reporting a verdict.

**Second pass (flipped):** Card 1 won 9/30 (30.0%), Card 2 won 21/30 (70.0%) — the same bias, same direction, same magnitude, reproduced independently. This is not noise; `claude-opus-4-8` has a stable, strong preference for whichever card appears second in this prompt structure.

**Combining both passes:** a pair only counts as decided if arm A wins in both orderings, or arm B wins in both orderings. Where the winner flips depending on which slot it was shown in, the pair is ambiguous — the position bias and the content signal are conflated and no confident call can be made for it, exactly analogous to the judge saying TIE.

| | Count |
|---|---|
| Robust A win (wins both orderings) | 13 |
| Robust B win (wins both orderings) | 2 |
| Ambiguous (winner flips with position) | 15 |

Position-robust A win rate: **86.7% (13/15)** — well past the 60% TRIM threshold, *if* you only look at the decisive subset. But that subset is half the data. **50% of all 30 pairs are ambiguous** — the judge's directional pick for them is not stable enough to trust in either direction.

The pre-registered rule's tie-fraction escape valve exists for exactly this situation: *"if more than a third of comparisons are ties, report REVERT with the note that the arms are indistinguishable."* An ambiguous, position-flip-sensitive pair is functionally the same null result as a judge-declared tie — the instrument could not render a stable, content-driven verdict. At 50%, well past the one-third bar, the rule's own logic points to REVERT.

**This is not "the arms are equal."** Among the pairs where the judge's opinion held steady regardless of presentation order, arm A won decisively (13-2). That's a real signal, not nothing. But the experiment as designed could only extract that signal from half the data; the other half is noise the methodology can't separate from content quality. The pre-registered rule doesn't have a carve-out for "trust the robust subset and ignore the ambiguous half" — and inventing one after seeing the data would be exactly the kind of post-hoc adjustment the pre-registration was meant to prevent. REVERT is the call the rule as written actually supports.

## Win table (raw, first pass — see above for why this number is unreliable on its own)

| Situation | Mode | A wins | B wins | Ties |
|---|---|---|---|---|
| s1 | teaching | 2 | 1 | 0 |
| s2 | teaching | 2 | 1 | 0 |
| s3 | parenting | 2 | 1 | 0 |
| s4 | parenting | 2 | 1 | 0 |
| s5 | managing | 2 | 1 | 0 |
| s6 | managing | 3 | 0 | 0 |
| s7 | coaching | 1 | 2 | 0 |
| s8 | coaching | 3 | 0 | 0 |
| s9 | parenting (carryover) | 3 | 0 | 0 |
| s10 | teaching (carryover) | 1 | 2 | 0 |
| **Total** | | **21** | **9** | **0** |

## Judge excerpts — position-robust decisive pairs

These three pairs kept the same winner in both the original and flipped orderings, so the reasoning below reflects genuine content judgment rather than position:

**s2 #2 (teaching, robust A win)** — original pass: *"Card 2 diagnoses the exact mechanism — that avoidance pays off precisely when the gap is visible and the readers' visible frustration blocks re-entry without losing face — whereas Card 1 stays a notch more abstract about resentment and status."* Flipped pass (arm A now Card 1): *"Card 1 diagnoses the precise mechanic — that visible frustration makes it harder for non-readers to re-enter without losing face — whereas Card 2 leans on more portable framing."* Same specific mechanism praised in arm A's card both times, regardless of which slot it sat in.

**s6 #1 (managing, robust A win)** — original: *"Card 1's read about them 'holding back to avoid embarrassing you' versus wondering if the place can teach them anything is a sharper [read of the status inversion]."* Flipped: *"Card 2's read — naming that they may be holding back to avoid embarrassing you, or quietly doubting the place can teach them — cuts closer to the specific psychology of this gap."* Identical diagnosis language tracked to arm A in both positions.

**s7 #2 (coaching, robust B win)** — original: *"Card 2 directly names the email and explicitly separates the kid from the parent's action, engaging the exact awkwardness, whereas Card 1 deliberately avoids the email and could apply to any playing-time talk."* Flipped: *"Card 1 names the concrete mechanic of the situation better ('your parent fought a battle they didn't win themselves') and pushes toward naming the actual skill gap."* Same content (the email-naming vs. avoiding it) tracked to arm B's card in both positions — the one clear case in this sample where a no-exemplar generation specifically out-diagnosed the exemplar arm on situational specificity.

## Position-bias check

**Confirmed and severe.** Card 1 win rate: first pass 26.7% (8/30), flipped pass 30.0% (9/30) — consistent across two independent judging runs, ~44 points below chance. This crosses the report's own ~65% flag threshold (in the opposite direction: Card 2, not Card 1, is the favored slot) and was the reason the flipped re-judging pass was run at all. The bias appears to be a `claude-opus-4-8` recency/second-mover preference specific to this side-by-side comparison prompt structure, not something correlated with arm assignment (the 15/15 position balance was verified before judging began).

## Identity carryover (s9)

Second confirmation, later date, same result as the original regression report: arm A diagnoses the "almost-18, shuts down about college/future" situation as **Competence** 3/3 times; arm B diagnoses it as **Identity** 3/3 times. Deterministic, unchanged from the first report. This situation also happened to be one of arm A's strongest wins in the quality judging (3-0, and its two individually-checked pairs were both in the robust-A-win set) — meaning the exemplar's version of this situation was judged as better-written *while also being diagnostically wrong* relative to the no-exemplar version. Quality and diagnostic accuracy are not the same axis, and this situation is the clearest place in the whole dataset where they pull apart.

## Script LCS check

Two flags over the 30-character threshold, both mild:
- s5 #2 [Commitment]: *"I need you shipping at the pace this role requires, and I am holding you to that"* — 36-char overlap with the exemplar's wise-feedback sentence structure.
- s8 #1 [Commitment]: *"From here, we hold each other to a higher standard than the scoreboard. I am hol[ding you to...]"* — 35-char overlap, same structural template (the "I am holding you to X because Y" commitment formula).

Both are structural-template echoes (the required wise-feedback sentence pattern the system prompt itself mandates), not diagnostic or narrative content leaks. Neither approaches the 9 verbatim exemplar phrases checked in the original regression report, and no hit exceeds 40 characters. This is consistent with, not a reversal of, the original report's Test 3 finding.

## Length check

Arm A mean: 2,830 bytes (n=30). Arm B mean: 3,222 bytes (n=30). Arm A is **12.2% shorter**. Tightness was the claimed benefit of the exemplar, and on raw length it delivers — arm A is not winning quality points by being longer; if anything it's winning (in the position-robust subset) while being more compact. This is the one clean, position-bias-free result in the exemplar's favor.

## The action

**Remove `shot` entirely** — the block in `send()` that builds `shot` from `EXEMPLAR.situation` / `EXEMPLAR.card` and prepends it to `allUser`. Since `GUARD`'s text ("the worked example above fixes format, tightness, and register only...") refers directly to an example that would no longer be sent, `GUARD` cannot survive unmodified — either delete the sentence that references "the worked example above," or rewrite the reminder to drop that clause and keep only the safety-override sentence. `EXEMPLAR` itself becomes dead code and should be removed along with the two constants once `shot` is gone.

Not proposing this edit be applied — report only, per instructions.

### Why not trim instead

Trimming was the pre-committed fallback if arm A won decisively. It didn't. The corrected data shows a real quality edge in the half of comparisons the position bias didn't swallow (13-2, 86.7%) — worth noting for anyone reconsidering the exemplar with a better-designed judge protocol (multiple judge models, or a rubric structure less prone to order effects) — but as this experiment was pre-registered and run, half the evidence is unusable, and the rule's own tie-fraction logic calls that REVERT. Combined with the original report's finding that arm B is already at 100% schema validity and the Identity situation flips diagnosis under the exemplar, there is no leg here to stand trimming on: the quality benefit is unproven at the pre-registered confidence bar, and the contamination cost is proven twice now.
