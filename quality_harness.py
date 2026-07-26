"""
Third Path — Blind Quality Comparison Harness (Trim vs Revert)
Reuses the extraction/transport machinery validated in exemplar_harness.py.
Generates n=3 arm-A / arm-B cards for 10 situations, pairs them blind,
and judges each pair with a fresh claude-opus-4-8 call against a fixed rubric.
"""

import anthropic
import json
import os
import re
import time
import random
from pathlib import Path

_token_file = os.environ.get("CLAUDE_SESSION_INGRESS_TOKEN_FILE", "")
_auth_token = open(_token_file).read().strip() if _token_file and os.path.exists(_token_file) else None
client = anthropic.Anthropic(auth_token=_auth_token) if _auth_token else anthropic.Anthropic()

GEN_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL = "claude-opus-4-8"
MAX_TOKENS = 1000
JUDGE_MAX_TOKENS = 600
RUNS_DIR = Path("quality-runs")
RUNS_DIR.mkdir(exist_ok=True)
N = 3

random.seed(20260726)  # deterministic position randomization, reproducible

# ── Extracted constants (identical to exemplar_harness.py) ──────────────────

ROLES = {
    "teaching":  {"who": "a teacher about a student (roughly ages 10–25)"},
    "parenting": {"who": "a parent about their own child (roughly ages 10–25)"},
    "managing":  {"who": "a manager about a young employee or direct report (roughly ages 18–25, early-career)"},
    "coaching":  {"who": "a coach about a young athlete or player on their team (roughly ages 10–25)"},
}

REGISTER = {
    "teaching":  "Write in a teacher's voice: one adult to many students, so the script has to survive a hallway or a two-minute aside, not a long private meeting.",
    "parenting": "Write in a parent's voice: the relationship is permanent and emotionally loaded, so the words can be warmer and blunter than any professional register, and the standard is a family expectation, not a policy.",
    "managing":  "Write in a manager's voice: this is a working adult with a job and a paycheck at stake, so use plain workplace language and treat them as an early-career colleague, never as a kid.",
    "coaching":  "Write in a coach's voice: short, physical, spoken in the moment at practice or on the sideline, where the team is always partly an audience.",
}

GUARD = "Reminder: the worked example above fixes format, tightness, and register only. Do not reuse its wording, its diagnosis, or its script. If this situation involves harm to the young person or to others, output only the safety object."

EXEMPLAR_SITUATION = "They agreed to the plan in front of everyone, and then I found out they have been telling the others privately that it is pointless and they are only going along with it."

EXEMPLAR_CARD = {
    "need": "Autonomy",
    "secondary": {"name": "Status"},
    "read": "They had no real say in the decision, so they complied where it was visible and resisted where it was safe. The private commentary is not really about the plan; it is how they buy back standing with the others after publicly going along with something they did not choose. Being overruled without being consulted reads as being treated as someone who carries out decisions rather than someone who helps make them.",
    "pull": {
        "collapse": "Enforcer",
        "instinct": "Confront the contradiction in front of the group, which humiliates them before the exact audience whose respect they were protecting and drives the resistance further underground."
    },
    "mentorMove": "Keep the plan itself non-negotiable, but treat the private objection as information you actually want. Go to them one to one, say you heard it, and ask for the argument out loud where it can still change how the plan runs.",
    "holdFirm": [
        "The plan stands and they are part of carrying it out.",
        "Disagreement comes to you directly rather than being routed around you."
    ],
    "stayFlexible": [
        "How much of the execution they help shape from here.",
        "Whether they raise objections privately with you first or in front of everyone."
    ],
    "forceLevel": {"level": 3, "label": "Collaboration"},
    "script": [
        {"phase": "Connection", "words": "I want to start with something true: you have real pull with the others. When you are behind something, people follow you into it. That is not a small thing."},
        {"phase": "Curiosity", "words": "So when you told them this was pointless, I want the actual reasoning, not the polite version. What is the part of this you think will not work?"},
        {"phase": "Collaboration", "words": "Here is what I would rather have happen. Bring that to me first, in the room where it can still change something. If you are right, the plan changes. If I still say we run it, at least you will know why, and you will have had a hand in how."},
        {"phase": "Commitment", "words": "I am asking you not to route it around me again. I am holding you to that because I think your judgment is good enough to make this thing better, not just good enough to survive it."}
    ],
    "longGame": "The skill is learning to put disagreement where it has power instead of where it is merely safe. Adults who can say the hard thing to the person who can act on it get trusted with decisions; adults who only say it sideways stay outside the room where decisions get made."
}


def build_system(mode):
    role = f"You are advising {ROLES[mode]['who']}. {REGISTER[mode]}"
    return f"""You are a mentoring reasoning engine grounded in David Yeager's "10 to 25" (the mentor mindset). {role}

CORE PRINCIPLE
When a young person resists, withdraws, argues, procrastinates, lies, avoids, or acts out, treat the behavior as an attempt to meet a developmental need; diagnose the need before solving the behavior. The situation may already have happened OR be one the adult is anticipating — handle both. When anticipated: diagnose the need that WILL be at stake, name the tempting setup (mandate/ban = Enforcer, quietly allow it = Protector), and write the script as how to INTRODUCE the expectation so it lands well.

THREE MINDSETS (the hinge of every answer)
- ENFORCER: high standards, low support — imposes, controls, punishes, lectures, shames.
- PROTECTOR: high support, low standards — rescues, excuses, drops the expectation to avoid conflict.
- MENTOR: high standards AND high support — holds the expectation while conferring respect and agency. Always the recommended path.
The adult's first instinct almost always collapses toward Enforcer OR Protector. Name which, then point to the mentor's third path.

MASTER NEED: STATUS & RESPECT
The deepest driver is the need to be respected and to matter. Confer status — treat the young person as a capable, developing peer, never a subordinate.

DIAGNOSTIC — WHICH NEED IS MOST THREATENED?
- Autonomy ("Do I have control?") — refusal, negotiation, power struggles, passive resistance.
- Status ("Do I matter?") — defensiveness, showing off, peer-driven choices, arguing, risk-taking.
- Belonging ("Do I fit?") — social anxiety, following peers, isolation, sensitivity to rejection.
- Competence ("Can I succeed?") — procrastination, giving up, avoidance, perfectionism, "I don't care."
- Identity ("Who am I becoming?") — experimentation, strong opinions, rejecting adult values, questions about the future.
Name the PRIMARY need, plus a SECONDARY need (one-line note on how it shows up) unless genuinely single-need.

LEAST FORCE NECESSARY
Recommend the least controlling intervention that still holds the standard; escalate only when lower levels fail: 1 Empathy → 2 Questions → 3 Collaboration → 4 Choices → 5 Natural consequences → 6 Enforced boundary.

STANDARDS FIRM, METHODS FLEXIBLE
Never negotiate the standard; widen the methods.

SCRIPT ARC: Connection → Curiosity → Collaboration → Commitment
The Commitment (or Connection) phase MUST include a wise-feedback statement: name the high standard AND your sincere belief they can meet it in the same breath (e.g., "I'm holding you to this because I have high standards and I know you can reach them"), adapted to this relationship. Required in every script.

FRAME GROWTH AS CAPABILITY, NOT DEFICIT
Normalize struggle as a brain getting MORE capable; never frame it as broken or not ready.

FRAMINGS (when relevant)
- Anxiety, nerves, or pressure central: reframe stress as the body mobilizing to perform — fuel, not a signal of inability (a racing heart is delivering oxygen, not announcing failure).
- Hollow motivation (grades-only, going through the motions, bare minimum): connect the standard to purpose and contribution — how meeting it lets them matter to people beyond themselves.

SAFETY OVERRIDE
If the situation involves potential harm to the young person or others — self-harm, suicidal thinking, abuse, neglect, threats of violence, or dangerous substance use — do NOT produce a script. Respond with ONLY {{ "safety": string }}: two or three plain sentences saying this is beyond a mentoring-conversation tool, that it must go promptly to the school counselor, administration, or appropriate professional per protocol (staff may have mandated-reporting duties), plus one supportive line about staying connected while the right people lead. No other fields.

OUTPUT
A worked example appears as the first exchange below. Match its structure, its tightness, and its plain speakable register; never reuse its content, its diagnosis, or its phrasing. Respond with ONLY a JSON object — no markdown, preamble, or code fences. No markdown/emphasis characters (* _ # backticks) inside string values; plain prose. Keep every field tight (1 to 3 sentences), in real, speakable language for this relationship. Schema:
{{
  "need": one of "Autonomy"|"Status"|"Belonging"|"Competence"|"Identity",
  "secondary": {{ "name": one of the five needs }} or null,
  "read": string — what's likely happening (or at stake), including the status/respect angle,
  "pull": {{ "collapse": "Enforcer"|"Protector", "instinct": string — the tempting reaction plus, in a few words, why it backfires }},
  "mentorMove": string — the third path in one or two sentences,
  "holdFirm": [string],
  "stayFlexible": [string],
  "forceLevel": {{ "level": 1-6, "label": "Empathy"|"Questions"|"Collaboration"|"Choices"|"Natural consequences"|"Enforced boundary" }},
  "script": [ {{ "phase": "Connection"|"Curiosity"|"Collaboration"|"Commitment", "words": string }} ],
  "longGame": string
}}"""


def build_prompt(mode, situation, arm):
    sys = build_system(mode)
    shot = []
    if arm == "A":
        shot = [
            {"role": "user", "content": EXEMPLAR_SITUATION},
            {"role": "assistant", "content": json.dumps(EXEMPLAR_CARD)},
        ]
    all_user = shot + [{"role": "user", "content": situation}]
    last = len(all_user) - 1
    msgs = []
    for i, m in enumerate(all_user):
        c = m["content"]
        if i == 0 and m["role"] == "user":
            c = sys + "\n\nSITUATION:\n" + c
        if i == last and m["role"] == "user":
            c = c + "\n\n" + GUARD
        msgs.append({"role": m["role"], "content": c})
    flat = "\n\n".join(
        ("ASSISTANT:\n" if m["role"] == "assistant" else "USER:\n") + m["content"]
        for m in msgs
    )
    flat += "\n\nRespond now as the assistant with ONLY the JSON object described above — no markdown, no code fences, no preamble."
    return flat


def extract_json(text):
    t = (text or "").strip()
    t = re.sub(r'^```(?:json)?', '', t, flags=re.IGNORECASE).rstrip('`').strip()
    try:
        return json.loads(t)
    except Exception:
        pass
    a, b = t.find("{"), t.rfind("}")
    if a != -1 and b > a:
        try:
            return json.loads(t[a:b+1])
        except Exception:
            pass
    raise ValueError(f"unparseable: {text[:200]}")


def run_one(mode, situation, arm, sit_id, n, retries=3):
    prompt = build_prompt(mode, situation, arm)
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=GEN_MODEL,
                max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text
            fname = RUNS_DIR / f"{arm}-{sit_id}-{n}.json"
            with open(fname, "w") as f:
                json.dump({"raw": raw, "mode": mode, "situation": situation, "arm": arm, "sit_id": sit_id, "n": n}, f, indent=2)
            card = extract_json(raw)
            return card, raw
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  FAILED after {retries} attempts: {e}")
                return None, None


def longest_common_substring(s1, s2):
    s1, s2 = s1.lower(), s2.lower()
    m = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    max_len = 0
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]:
                m[i][j] = m[i-1][j-1] + 1
                max_len = max(max_len, m[i][j])
            else:
                m[i][j] = 0
    return max_len


def render_card(card):
    """Human-readable rendering for judge, with no arm-identifying artifacts."""
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


# ═══════════════════════════════════════════════════════════════════════════
# SITUATIONS
# ═══════════════════════════════════════════════════════════════════════════

SITUATIONS = [
    ("s1",  "teaching",  "A student handed in work far better than anything they have produced before, and I genuinely cannot tell if it is a breakthrough or if someone else did it."),
    ("s2",  "teaching",  "Half the class did the reading and half clearly did not, and the half that did is getting visibly annoyed at carrying discussions."),
    ("s3",  "parenting", "My kid announced at dinner they are done with church and are not going anymore."),
    ("s4",  "parenting", "My teenager asked me a hard question about something I did at their age, and I froze instead of answering."),
    ("s5",  "managing",  "A junior shipped something with a mistake a customer caught, and now they are triple-checking everything and velocity has cratered."),
    ("s6",  "managing",  "My newest hire is better at part of the job than I am and we both know it."),
    ("s7",  "coaching",  "A player's parent emailed me arguing their kid should be starting, and the kid clearly knows about the email."),
    ("s8",  "coaching",  "My team won big and played selfish, ugly ball the entire game."),
    ("s9",  "parenting", "My almost-18-year-old shuts down every time college or life after graduation comes up."),  # carryover — Identity flip
    ("s10", "teaching",  "A student who clearly studied did poorly and is convinced they are just bad at this subject."),  # carryover — stable Competence
]

print("=" * 70)
print("QUALITY COMPARISON HARNESS — GENERATION")
print("=" * 70)

generated = {}  # sit_id -> {"A": [cards], "B": [cards]}

for sit_id, mode, situation in SITUATIONS:
    generated[sit_id] = {"A": [], "B": []}
    for arm in ["A", "B"]:
        for n in range(1, N + 1):
            print(f"  [{arm}] {sit_id} ({mode}) #{n}...")
            card, raw = run_one(mode, situation, arm, sit_id, n)
            generated[sit_id][arm].append(card)
            time.sleep(0.4)

print("\nGeneration complete.")

# ═══════════════════════════════════════════════════════════════════════════
# PAIRING + BLIND JUDGING
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("BLIND PAIRWISE JUDGING")
print("=" * 70)

pairs = []  # list of dicts: sit_id, mode, situation, n, cardA, cardB, position_key, judge_raw, pick, dims

# Build all 30 pairs first, with balanced position randomization (15/15)
position_assignments = [True] * 15 + [False] * 15  # True = A is "Card 1"
random.shuffle(position_assignments)

pair_idx = 0
for sit_id, mode, situation in SITUATIONS:
    for n in range(N):
        cardA = generated[sit_id]["A"][n]
        cardB = generated[sit_id]["B"][n]
        if cardA is None or cardB is None:
            print(f"  SKIP {sit_id} #{n+1} — missing card (A={cardA is not None}, B={cardB is not None})")
            pair_idx += 1
            continue

        a_is_card1 = position_assignments[pair_idx]
        pair_idx += 1

        if a_is_card1:
            card1_text, card2_text = render_card(cardA), render_card(cardB)
        else:
            card1_text, card2_text = render_card(cardB), render_card(cardA)

        print(f"  Judging {sit_id} #{n+1} (A is Card {'1' if a_is_card1 else '2'})...")
        judge_raw = judge_pair(situation, card1_text, card2_text)
        pick, dims = parse_judge(judge_raw)

        # Translate pick back to arm
        if pick == "1":
            winner_arm = "A" if a_is_card1 else "B"
        elif pick == "2":
            winner_arm = "B" if a_is_card1 else "A"
        else:
            winner_arm = "TIE"

        pair_record = {
            "sit_id": sit_id, "mode": mode, "situation": situation, "n": n + 1,
            "a_is_card1": a_is_card1, "pick": pick, "winner_arm": winner_arm,
            "dims": dims, "judge_raw": judge_raw,
        }
        pairs.append(pair_record)

        with open(RUNS_DIR / f"judge-{sit_id}-{n+1}.json", "w") as f:
            json.dump(pair_record, f, indent=2)

        time.sleep(0.4)

print("\nJudging complete.")

with open(RUNS_DIR / "all_pairs.json", "w") as f:
    json.dump(pairs, f, indent=2)

# ═══════════════════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

total = len(pairs)
a_wins = sum(1 for p in pairs if p["winner_arm"] == "A")
b_wins = sum(1 for p in pairs if p["winner_arm"] == "B")
ties = sum(1 for p in pairs if p["winner_arm"] == "TIE")

print(f"\nTotal pairs judged: {total}")
print(f"A wins: {a_wins}  B wins: {b_wins}  Ties: {ties}")

non_tie = a_wins + b_wins
if non_tie > 0:
    a_pct = 100 * a_wins / non_tie
    print(f"A win rate (excluding ties): {a_pct:.1f}% ({a_wins}/{non_tie})")
else:
    a_pct = None

tie_frac = ties / total if total else 0
print(f"Tie fraction: {tie_frac:.1%}")

if tie_frac > 1/3:
    verdict = "REVERT (ties exceed 1/3, arms indistinguishable per rule)"
elif a_pct is not None and a_pct > 60:
    verdict = "TRIM"
else:
    verdict = "REVERT"

print(f"\nVERDICT: {verdict}")

# Per-situation win table
print("\nPer-situation:")
by_sit = {}
for p in pairs:
    by_sit.setdefault(p["sit_id"], {"A": 0, "B": 0, "TIE": 0})
    by_sit[p["sit_id"]][p["winner_arm"]] += 1
for sit_id, mode, situation in SITUATIONS:
    r = by_sit.get(sit_id, {"A": 0, "B": 0, "TIE": 0})
    print(f"  {sit_id} ({mode}): A={r['A']} B={r['B']} TIE={r['TIE']}")

# Position-bias check
card1_wins = sum(1 for p in pairs if (p["pick"] == "1"))
card2_wins = sum(1 for p in pairs if (p["pick"] == "2"))
pos_total = card1_wins + card2_wins
print(f"\nPosition bias: Card1={card1_wins} Card2={card2_wins}", end="")
if pos_total:
    print(f" ({100*card1_wins/pos_total:.1f}% Card1)")
else:
    print()

# Identity carryover (s9)
print("\n[Identity carryover check — s9]")
s9_A_needs = [c.get("need") for c in generated["s9"]["A"] if c]
s9_B_needs = [c.get("need") for c in generated["s9"]["B"] if c]
print(f"  Arm A primary needs: {s9_A_needs}")
print(f"  Arm B primary needs: {s9_B_needs}")

# Script LCS check
print("\n[Script LCS check — arm A script lines vs exemplar script lines]")
exemplar_lines = [s["words"] for s in EXEMPLAR_CARD["script"]]
lcs_flags = []
for sit_id, mode, situation in SITUATIONS:
    for n, card in enumerate(generated[sit_id]["A"]):
        if not card:
            continue
        for s in card.get("script", []) or []:
            line = s.get("words", "")
            for ex_line in exemplar_lines:
                lcs = longest_common_substring(line, ex_line)
                if lcs > 30:
                    lcs_flags.append({"sit_id": sit_id, "n": n+1, "phase": s.get("phase"), "lcs_len": lcs, "line": line[:80], "exemplar_line": ex_line[:80]})
print(f"  Flags (>30 chars): {len(lcs_flags)}")
for f in lcs_flags:
    print(f"    {f['sit_id']} #{f['n']} [{f['phase']}] lcs={f['lcs_len']}: {f['line']}")

# Length check
print("\n[Length check — mean serialized card bytes]")
a_lens = [len(json.dumps(c)) for sit_id, mode, situation in SITUATIONS for c in generated[sit_id]["A"] if c]
b_lens = [len(json.dumps(c)) for sit_id, mode, situation in SITUATIONS for c in generated[sit_id]["B"] if c]
mean_a = sum(a_lens) / len(a_lens) if a_lens else 0
mean_b = sum(b_lens) / len(b_lens) if b_lens else 0
print(f"  Arm A mean bytes: {mean_a:.0f} (n={len(a_lens)})")
print(f"  Arm B mean bytes: {mean_b:.0f} (n={len(b_lens)})")
print(f"  Difference: {mean_a - mean_b:+.0f} bytes ({100*(mean_a-mean_b)/mean_b:+.1f}%)" if mean_b else "")

# Save full summary
summary = {
    "total": total, "a_wins": a_wins, "b_wins": b_wins, "ties": ties,
    "a_win_pct_excl_ties": a_pct, "tie_fraction": tie_frac, "verdict": verdict,
    "by_situation": by_sit,
    "position_bias": {"card1_wins": card1_wins, "card2_wins": card2_wins},
    "s9_identity_carryover": {"A": s9_A_needs, "B": s9_B_needs},
    "lcs_flags": lcs_flags,
    "length": {"mean_a_bytes": mean_a, "mean_b_bytes": mean_b, "n_a": len(a_lens), "n_b": len(b_lens)},
}
with open(RUNS_DIR / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

print("\nAll data saved to quality-runs/")
print("Summary in quality-runs/summary.json")
