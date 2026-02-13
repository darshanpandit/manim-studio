---
name: screenplay-reviewer
description: Use when reviewing, critiquing, or iterating on a .screenplay file. Produces structured feedback on narrative quality, pacing, voice usage, and visual design. Invoke after screenplay-writer to iterate toward a better script.
---

# Reviewing Screenplays for ManimCE

Critique `.screenplay` files against narrative, structural, and pedagogical standards. Output actionable feedback that the writer can use to revise. This skill is the editorial counterpart to `screenplay-writer`.

## Process

1. **Read the screenplay** — Parse header, data block, voices, all beats.
2. **Read project context** — Check `CLAUDE.md` for available assets, style, and conventions.
3. **Run all critique passes** (see below) — structural, narrative, voice, visual, pacing, audience.
4. **Produce the Review** — Structured output with verdicts, specific line references, and rewrite suggestions.
5. **Assign a grade** — A/B/C/D with justification.

## Critique Passes

Run each pass independently. A screenplay can score well on structure but fail on narrative.

### Pass 1: Structural Integrity

Check the DSL is well-formed and complete.

| Check | Pass | Fail |
|-------|------|------|
| Beat count | 3-8 beats | < 3 (thin) or > 8 (bloated) |
| Every beat has voiceover | All beats have `>` lines | Missing voiceover |
| Every beat has visual | All beats have SHOW/ANIMATE/TITLE/TEXT | Talking head beat |
| DATA block complete | All referenced data specified | Missing source/params |
| VOICES block present (if multi-voice) | Declared before use | Tags without declaration |
| FADEOUT: all at end | Present | Missing cleanup |
| On-screen text length | Max 6 words/line, 2 lines | Wall of text |
| No orphan directives | Every SHOW/ANIMATE is near voiceover | Disconnected visuals |

### Pass 2: Narrative Quality

The hardest pass. Evaluate the writing itself.

**Opening (Beat 1):**
- Does it hook within the first 2 sentences?
- Is there a question, mystery, or surprise?
- Would you keep watching? Be honest.

**Middle (Beats 2-N):**
- One idea per beat? Or cramming?
- Does each beat build on the previous one?
- Are transitions smooth or jarring?
- Is the skeptic earning their keep or just saying "wow"?

**Closing (Last beat):**
- Is there resolution?
- Does it tease what's next without being cheap?
- Would the viewer feel satisfied AND curious?

**Line-by-line:**
- Flag any academic/stilted phrasing ("It can be observed that...", "We note that...")
- Flag filler ("Let's take a look at...", "So basically...")
- Flag over-explanation (explaining what the viewer can see)
- Flag under-explanation (jargon without setup)
- Flag missed humor opportunities
- Flag lines that would sound flat when spoken aloud (read every line aloud mentally)

**Anti-patterns to catch:**

| Anti-pattern | Example | Fix |
|-------------|---------|-----|
| Lecture mode | "The Kalman Filter is defined as..." | "Watch what happens when..." |
| Sycophantic skeptic | "Wow, that's amazing!" | Give the skeptic real objections |
| Rhetorical dead-end | "Isn't that interesting?" (no follow-up) | Answer the question or cut it |
| Monotone dialogue | 5 narrator lines, 1 skeptic line, repeat | Interleave more naturally |
| Explaining the visual | "As you can see, the ellipse is shrinking" | "The ellipse shrinks." or just let it shrink |
| Throat-clearing | "Now let's move on to discuss..." | Just start the next topic |
| Hedging | "This is sort of like a weighted average" | Commit: "This IS a weighted average" |

### Pass 3: Voice & Prosody

Evaluate multi-voice dynamics and style/prosody usage.

| Check | Good | Bad |
|-------|------|-----|
| Voice balance | Skeptic speaks 20-35% of lines | < 15% (decoration) or > 40% (hijacking) |
| Skeptic role | Asks real questions, pushes back, represents viewer | Cheerleader, echo chamber |
| Style variation | 3-5 style switches per 5 minutes | None (monotone) or > 10 (distracting) |
| Prosody usage | Rate changes on 2-4 key lines for emphasis | None or on every other line |
| Style placement | newscast for authority, whispering for asides, hopeful for closings | Random style assignment |
| Natural transitions | Voice switches follow conversational rhythm | Abrupt mid-thought switches |
| Distinct personalities | Each voice has a recognizable character | Both sound the same |

**Skeptic quality rubric:**
- **A**: Skeptic asks questions the viewer is thinking, challenges claims, earns respect
- **B**: Skeptic asks good questions but doesn't push back enough
- **C**: Skeptic is just a prompt for the narrator to continue
- **D**: Skeptic adds nothing — could be removed without loss

### Pass 4: Visual Design

Evaluate the visual storytelling.

| Check | Pass | Fail |
|-------|------|------|
| Show before tell | Visual appears before/during explanation | Equation first, visual later |
| Visual variety | Mix of dots, paths, ellipses, diagrams, text | Same type of visual repeated |
| Animation purpose | Every animation reveals something | Animation for decoration |
| Pause after insight | PAUSE follows key visual moments | Rush through insights |
| Progressive disclosure | Elements build up, not all at once | Everything appears simultaneously |
| Screen real estate | Visuals use the frame well | Everything cramped in center |
| Cleanup between sections | FADEOUT before new topic | Clutter accumulation |

### Pass 5: Pacing & Runtime

Estimate runtime and check pacing.

**Word count to runtime:**
- Average spoken pace: ~150 words/minute
- With pauses and animations: ~120 words/minute effective
- Count all voiceover words, divide by 120 = estimated minutes

**Pacing checks:**

| Issue | Sign | Fix |
|-------|------|-----|
| Too fast | > 170 words/min, no PAUSE directives | Add pauses, cut words |
| Too slow | < 100 words/min, excessive pauses | Tighten prose, reduce pauses |
| Front-loaded | Beat 1 has 60% of the words | Redistribute |
| Back-loaded | Conclusion is longer than the hook | Cut conclusion, expand middle |
| Monotone rhythm | All beats same length | Vary: short punchy + long flowing |
| Dead air | PAUSE: long with nothing visual happening | Add subtle animation during pause |

**Target runtimes by video type:**
- Hook/opener: 1-2 minutes
- Single concept: 3-5 minutes
- Full chapter (single file): 6-10 minutes
- Comparison/capstone: 4-7 minutes

### Pass 6: Audience Calibration

For this project: mature academic audience (PhD-level, cross-disciplinary).

| Check | Good | Bad |
|-------|------|-----|
| Intellectual respect | References connections to their fields | Explains what a matrix is |
| Cross-disciplinary hooks | "If you know BLUP..." / "In econometrics..." | Only one field's perspective |
| Appropriate depth | Shows the proof sketch, not just the result | Hand-waves everything |
| Honest limitations | "This breaks when..." | "This always works" |
| Humor caliber | Dry wit, field-specific jokes, understatement | Forced jokes, puns |
| Citation density | 1-2 per major claim | None or excessive |
| Jargon handling | Uses terms, doesn't over-define | Defines "matrix" but uses "MMSE" without setup |

## Output Format

Structure the review as follows:

```
# Screenplay Review: [Title]

## Grade: [A/B/C/D]

## What Works
- [2-3 specific strengths with line references]

## Critical Issues
- [Numbered list of problems that MUST be fixed]
- Each issue: what's wrong, where (beat #), specific suggestion

## Suggested Improvements
- [Numbered list of nice-to-have improvements]
- Each: what could be better, concrete rewrite suggestion

## Pass Results
| Pass | Grade | Notes |
|------|-------|-------|
| Structure | A/B/C/D | [one-line summary] |
| Narrative | A/B/C/D | [one-line summary] |
| Voice/Prosody | A/B/C/D | [one-line summary] |
| Visual Design | A/B/C/D | [one-line summary] |
| Pacing | A/B/C/D | [one-line summary] |
| Audience | A/B/C/D | [one-line summary] |

## Runtime Estimate
- Word count: [N]
- Estimated runtime: [M] minutes
- Target: [T] minutes
- Verdict: [on target / too short / too long]

## Rewrite Priority
1. [Most important fix — do this first]
2. [Second priority]
3. [Third priority]
```

## Grading Scale

| Grade | Meaning | Action |
|-------|---------|--------|
| **A** | Ship it. Minor polish only. | Proceed to code generation |
| **B** | Good foundation, needs one more pass. | Revise and re-review |
| **C** | Structural or narrative problems. | Significant rewrite needed |
| **D** | Fundamental issues with approach. | Rethink the concept |

**Grade honestly.** A first draft is almost never an A. That's fine — iteration is the point.

## Iteration Protocol

When used in a write-review-revise loop:

1. **Draft 1** → Review → expect C or B
2. **Draft 2** (addressing Critical Issues) → Review → expect B or B+
3. **Draft 3** (addressing Suggested Improvements) → Review → expect A or B+
4. If still not A after 3 iterations, the concept might need rethinking

**Between iterations:**
- Only address the review feedback — don't introduce new ideas
- The reviewer should acknowledge what was fixed
- New issues discovered in revision get flagged as new, not repeated

## Common Reviewer Mistakes

| Mistake | Fix |
|---------|-----|
| Being too nice | If you wouldn't watch it, say so |
| Rewriting the whole thing | Give specific fixes, not a new screenplay |
| Ignoring the data/visual layer | Visuals carry 50% of the teaching |
| Focusing only on text | Prosody and pacing matter as much as words |
| Not reading aloud | Every voiceover line must sound natural spoken |
| Contradicting project CLAUDE.md | Check conventions before flagging "issues" |
