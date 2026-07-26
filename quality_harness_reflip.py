"""
Position-bias remediation pass.
The first judging pass showed Card2 winning 73.3% of pairs regardless of arm
(when A was Card1: 7-8 coin flip; when A was Card2: 14-1 sweep) — a severe
position bias that fully confounds the raw 70% arm-A win rate.
Per the pre-registered contingency, re-judge every pair with positions
flipped and combine: only count a pair as decided if both orderings agree
on the winning arm.
"""

import anthropic
import json
import os
import time
from pathlib import Path

_token_file = os.environ.get("CLAUDE_SESSION_INGRESS_TOKEN_FILE", "")
_auth_token = open(_token_file).read().strip() if _token_file and os.path.exists(_token_file) else None
client = anthropic.Anthropic(auth_token=_auth_token) if _auth_token else anthropic.Anthropic()

JUDGE_MODEL = "claude-opus-4-8"
JUDGE_MAX_TOKENS = 600
RUNS_DIR = Path("quality-runs")

import re

def render_card(card):
    lines = []
    need = card.get("need", "?")
    sec = card.get("secondary") or {}
    sec_name = sec.get("name") if isinstance(sec, dict) else None
    lines.append(f"NEED: {need}" + (f" (secondary: {sec_name})" if sec_name else ""))
    lines.append(f"\nTHE READ:\n{card.get('read','')}")
    pull = card.get("pull", {}) or {}
    lines.append(f"\nYOUR PULL ({pull.get('collapse','?')}):\n{pull.get('instinct','')}")
    lines.append(f"\nTHE MENTOR MOVE:\n{card.get('mentorMove','')}")
    hf = card.get("holdFirm", []) or []
    sf = card.get("stayFlexible", []) or []
    lines.append("\nHOLD FIRM:\n" + "\n".join(f"- {x}" for x in hf))
    lines.append("\nSTAY FLEXIBLE:\n" + "\n".join(f"- {x}" for x in sf))
    fl = card.get("forceLevel", {}) or {}
    lines.append(f"\nFORCE LEVEL: {fl.get('level','?')} ({fl.get('label','?')})")
    lines.append("\nSCRIPT:")
    for s in card.get("script", []) or []:
        lines.append(f"[{s.get('phase','?')}] \"{s.get('words','')}\"")
    lines.append(f"\nLONG GAME:\n{card.get('longGame','')}")
    return "\n".join(lines)


JUDGE_RUBRIC = """You are comparing two coaching cards written for an adult navigating a hard moment with a young person. Judge only on these dimensions — not on formatting, length, or JSON:
1. SPEAKABILITY — could the adult say the script lines out loud, tomorrow, without sounding scripted?
2. SPECIFICITY — does the diagnosis engage this exact situation, or would it fit any situation in the genre?
3. TIGHTNESS — does every sentence earn its place, or does it pad?
4. HONESTY OF THE HARD PART — does it keep the standard and name the uncomfortable thing, or does it soften into generic warmth?
Pick the better card overall, or TIE if genuinely indistinguishable. State your pick first, then one sentence per dimension.

Respond in exactly this format:
PICK: 1|2|TIE
SPEAKABILITY: <one sentence>
SPECIFICITY: <one sentence>
TIGHTNESS: <one sentence>
HONESTY: <one sentence>"""


def judge_pair(situation, card1_text, card2_text, retries=3):
    prompt = f"""SITUATION:
{situation}

CARD 1:
{card1_text}

CARD 2:
{card2_text}

{JUDGE_RUBRIC}"""
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=JUDGE_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  JUDGE FAILED after {retries} attempts: {e}")
                return None


def parse_judge(text):
    if not text:
        return None, {}
    pick_m = re.search(r'PICK:\s*(1|2|TIE)', text, re.IGNORECASE)
    pick = pick_m.group(1).upper() if pick_m else None
    dims = {}
    for dim in ["SPEAKABILITY", "SPECIFICITY", "TIGHTNESS", "HONESTY"]:
        m = re.search(rf'{dim}:\s*(.+?)(?=\n[A-Z]+:|$)', text, re.IGNORECASE | re.DOTALL)
        dims[dim] = m.group(1).strip() if m else ""
    return pick, dims


pairs = json.load(open(RUNS_DIR / "all_pairs.json"))

print(f"Re-judging {len(pairs)} pairs with flipped positions...")

flipped_pairs = []
for p in pairs:
    sit_id, n = p["sit_id"], p["n"]
    cardA = json.load(open(RUNS_DIR / f"A-{sit_id}-{n}.json"))
    cardB = json.load(open(RUNS_DIR / f"B-{sit_id}-{n}.json"))
    cardA = json.loads(cardA["raw"])
    cardB = json.loads(cardB["raw"])

    # Flip: opposite of original a_is_card1
    a_is_card1_flipped = not p["a_is_card1"]

    if a_is_card1_flipped:
        card1_text, card2_text = render_card(cardA), render_card(cardB)
    else:
        card1_text, card2_text = render_card(cardB), render_card(cardA)

    print(f"  Re-judging {sit_id} #{n} (flipped: A is now Card {'1' if a_is_card1_flipped else '2'})...")
    judge_raw = judge_pair(p["situation"], card1_text, card2_text)
    pick, dims = parse_judge(judge_raw)

    if pick == "1":
        winner_arm = "A" if a_is_card1_flipped else "B"
    elif pick == "2":
        winner_arm = "B" if a_is_card1_flipped else "A"
    else:
        winner_arm = "TIE"

    flipped_record = {
        "sit_id": sit_id, "mode": p["mode"], "situation": p["situation"], "n": n,
        "a_is_card1": a_is_card1_flipped, "pick": pick, "winner_arm": winner_arm,
        "dims": dims, "judge_raw": judge_raw,
        "original_winner_arm": p["winner_arm"],
    }
    flipped_pairs.append(flipped_record)

    with open(RUNS_DIR / f"judge-flipped-{sit_id}-{n}.json", "w") as f:
        json.dump(flipped_record, f, indent=2)

    time.sleep(0.4)

with open(RUNS_DIR / "all_pairs_flipped.json", "w") as f:
    json.dump(flipped_pairs, f, indent=2)

print("\n" + "=" * 70)
print("POSITION-CONTROLLED RESULTS")
print("=" * 70)

card1_wins_flip = sum(1 for p in flipped_pairs if p["pick"] == "1")
card2_wins_flip = sum(1 for p in flipped_pairs if p["pick"] == "2")
print(f"\nFlipped-pass position bias: Card1={card1_wins_flip} Card2={card2_wins_flip} ({100*card1_wins_flip/len(flipped_pairs):.1f}% Card1)")

# Combine: agree = both passes give same winner_arm; disagree = position flips the verdict -> ambiguous
agree_a = 0
agree_b = 0
agree_tie = 0
disagree = 0
combined = []
for orig, flip in zip(pairs, flipped_pairs):
    assert orig["sit_id"] == flip["sit_id"] and orig["n"] == flip["n"]
    if orig["winner_arm"] == flip["winner_arm"]:
        if orig["winner_arm"] == "A":
            agree_a += 1
        elif orig["winner_arm"] == "B":
            agree_b += 1
        else:
            agree_tie += 1
        combined.append({"sit_id": orig["sit_id"], "n": orig["n"], "mode": orig["mode"],
                          "robust_winner": orig["winner_arm"], "orig": orig["winner_arm"], "flipped": flip["winner_arm"]})
    else:
        disagree += 1
        combined.append({"sit_id": orig["sit_id"], "n": orig["n"], "mode": orig["mode"],
                          "robust_winner": "AMBIGUOUS", "orig": orig["winner_arm"], "flipped": flip["winner_arm"]})

print(f"\nPosition-robust (both orderings agree): A={agree_a} B={agree_b} TIE={agree_tie}")
print(f"Position-confounded (orderings disagree, excluded): {disagree}")

decisive = agree_a + agree_b
if decisive > 0:
    robust_a_pct = 100 * agree_a / decisive
    print(f"\nRobust A win rate (excl. ties+ambiguous): {robust_a_pct:.1f}% ({agree_a}/{decisive})")
else:
    robust_a_pct = None
    print("\nNo decisive position-robust results.")

total_considered = agree_a + agree_b + agree_tie
ambiguous_frac = disagree / len(pairs)
print(f"Ambiguous (position-flip-sensitive) fraction: {ambiguous_frac:.1%}")

with open(RUNS_DIR / "position_controlled_summary.json", "w") as f:
    json.dump({
        "flipped_pass_position_bias": {"card1": card1_wins_flip, "card2": card2_wins_flip},
        "agree_a": agree_a, "agree_b": agree_b, "agree_tie": agree_tie, "disagree": disagree,
        "robust_a_win_pct": robust_a_pct, "ambiguous_fraction": ambiguous_frac,
        "combined": combined,
    }, f, indent=2, default=str)

print("\nSaved to quality-runs/position_controlled_summary.json")

print("\nPer-pair robust outcome:")
for c in combined:
    print(f"  {c['sit_id']} #{c['n']} ({c['mode']}): orig={c['orig']} flipped={c['flipped']} -> {c['robust_winner']}")
