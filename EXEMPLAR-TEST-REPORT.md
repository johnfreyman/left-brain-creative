# Third Path — Exemplar Regression Report

Model: `claude-sonnet-4-6`, max_tokens 1000, n=3 per situation per arm, 93 total API calls (57 arm A, 36 arm B). `buildSystem()`, `ROLES`, `REGISTER`, `EXEMPLAR`, `GUARD` extracted programmatically from `The_Third_Path__publishable.html` and called directly; transport replicates `send()` message assembly and `askAI()`'s flatten-to-one-string format exactly (`USER:\n` / `ASSISTANT:\n` labels, trailing "respond now" line). Raw responses for every run are in `runs/`.

## Verdict: **TRIM**

Not ship, not revert. The blocking safety gate holds in both arms, wording never leaks, and force-level/collapse-type anchoring toward the exemplar's own values (3/Collaboration, Enforcer) did not materialize. But schema validity is **already 100% with the exemplar removed** (arm B = 36/36), and there is one real, deterministic, n=3-confirmed diagnostic flip in Test 2 that the exemplar causes and arm B does not. The exemplar is buying no measurable format-fidelity gain on this model while carrying a live, demonstrated contamination cost on at least one situation. The pre-agreed remedy — cut `EXEMPLAR.card.read` and `.longGame` to one sentence each — is the right move: it keeps the structural demonstration (schema, tightness, phase order) while shrinking the semantic surface that appears to be doing the dragging.

## Per-test results

| Test | Result | Arm A | Arm B | A vs B distinguishable? |
|---|---|---|---|---|
| 1. Safety branch (blocking) | **PASS** | 6/6 teaching+parenting → safety-only object, 0 leaked card fields | 6/6 same | No — identical behavior, both clean |
| 2. Need contamination | **FLAG** (see below) | 3 of 4 situations diagnosed correctly; Identity situation → Competence 3/3 | All 4 situations diagnosed correctly, 3/3 each | **Yes** — this is the one test that actually caught something |
| 3. Wording echo | **PASS** | 0 verbatim hits on 9 exemplar phrases; 0 LCS >40 chars vs exemplar `read`/`longGame` across all 57 arm-A runs | n/a (echo test is arm-A only) | — |
| 4. Register separation (judgment) | **CAUTION**, not exemplar-attributable | Parenting and managing cleanly separated (warm/no-policy vs. workplace/role language). Teaching and coaching blur — both open "Hey, I..." and neither reliably uses classroom or court/practice nouns; one teaching run even said "back in the game." Blind-read accuracy: confident on 2/4, coin-flip on the other 2 | n/a (arm-A only per spec) | Can't isolate exemplar effect — test wasn't run as A/B |
| 5. Force-level anchoring | **PASS** | 9/9 in expected ranges; **0/9 landed on level 3** (the exemplar's level) | 8/9 in expected ranges; 4/9 landed on 3 (all within their own valid ranges) | Yes — and the anchoring, if anything, ran opposite the hypothesis |
| 6. Collapse anchoring | **PASS**, proves nothing | Protector 6/6 (correct answer both times) | Protector 6/6 (correct answer both times) | **No** — identical in both arms, situations were not sensitive enough to catch anchoring even if present |
| 7. Anticipatory branch (judgment) | **PASS** | 3/3 forward-looking ("before they have done a single thing," "first week," "Monday") | n/a (arm-A only per spec) | — |
| 8. Multi-turn | **PASS** | 3/3 escalated force level (3→5, 3→4, 3→4); all 3 turn-2 reads substantively reference the failed first attempt ("a step past the original stall," "the conversation itself became the escape hatch") | n/a (arm-A only per spec) | — |

### Test 2 detail — the one real finding

The pre-registered fail conditions (≥3/4 situations pulled to Autonomy-primary, or Status-secondary in ≥10/12 arm-A runs) did **not** trigger — arm A never returned Autonomy as primary, and Status appeared as secondary 0/12 times. By that literal bar, Test 2 passes.

But the per-situation breakdown surfaces something the pre-registered conditions didn't anticipate:

| Situation (mode) | Expected | Arm A (3 runs) | Arm B (3 runs) |
|---|---|---|---|
| Bombed a studied-for test (teaching) | Competence | Competence, Competence, Competence | Competence, Competence, Competence |
| New mid-year student, sits apart (teaching) | Belonging | Belonging, Belonging, Belonging | Belonging, Belonging, Belonging |
| Almost-18, shuts down about college/future (parenting) | **Identity** | **Competence, Competence, Competence** | **Identity, Identity, Identity** |
| Showboats after good plays (coaching) | Status | Status, Status, Status | Status, Status, Status |

The Identity situation flips its primary/secondary pair wholesale depending on arm — deterministically, 3/3 vs 3/3, nothing else changed. Arm A's own reasoning is coherent (it reframes "shuts down about the future" as fear-of-incompetence rather than an identity crisis), but the fact that it's the *only* situation that moves, and moves in lockstep across all three samples, while every other situation stays put, is a clean signal that the exemplar is exerting real pull on ambiguous need-diagnosis calls — just not in the direction (Autonomy/Status mimicry) the test predicted. This is exactly the kind of contamination the harness exists to catch, and it caught it.

## Health metrics (arm A, all 57 non-safety-excluded runs)

- Distinct primary needs: 5 of 5 — `{Competence: 36, Status: 3, Belonging: 3, Identity: 3, Autonomy: 3}` (target ≥3, met — though Competence dominance reflects the specific situations selected across tests, not a structural bias toward the exemplar's own need)
- Both collapse types present: **yes** — Enforcer 13, Protector 35 (target: both present, met)
- Force-level spread: 5 distinct levels used — `1, 2, 3, 4, 5` (target ≥3, met)

## Schema validity rate

**Arm A: 57/57 (100%). Arm B: 36/36 (100%).**

This is the number that was supposed to justify the exemplar's existence. Arm B — zero-shot, no worked example — is already at 100% structural validity on `claude-sonnet-4-6`. The exemplar is not measurably improving format fidelity on this model; every dollar of contamination risk it introduces (per Test 2) is currently unpaid for.

## Recommended diff

Per the pre-agreed remedy for a Test 2 finding: cut `EXEMPLAR.card.read` and `EXEMPLAR.card.longGame` to one sentence each, keeping the schema, phase order, tightness, and register demonstration intact while shrinking the semantic surface that's dragging ambiguous diagnoses.

```diff
       read: "They had no real say in the decision, so they complied where it was visible and resisted where it was safe. The private commentary is not really about the plan; it is how they buy back standing with the others after publicly going along with something they did not choose. Being overruled without being consulted reads as being treated as someone who carries out decisions rather than someone who helps make them.",
+      read: "They had no real say in the decision, so they complied where it was visible and resisted where it was safe.",
```

```diff
       longGame: "The skill is learning to put disagreement where it has power instead of where it is merely safe. Adults who can say the hard thing to the person who can act on it get trusted with decisions; adults who only say it sideways stay outside the room where decisions get made."
+      longGame: "The skill is learning to put disagreement where it has power instead of where it is merely safe."
```

Not recommended: a second, safety-shaped exemplar. Test 1 passed cleanly in both arms — the safety branch is not at risk, so the spec's stated trigger for that addition isn't met.

Separately, outside the scope of this exemplar test: Test 4 surfaced a teaching/coaching register blur that appears to be a `REGISTER` prompt weakness independent of the exemplar (the exemplar itself is deliberately domain-neutral, and this test wasn't run as an A/B, so the exemplar can't be blamed here). Worth a follow-up pass on `REGISTER.teaching` and `REGISTER.coaching` to force more distinct vocabulary (explicit "class"/"student" vs. "practice"/"team" anchoring), but that's a separate fix from the one this harness was built to evaluate.
