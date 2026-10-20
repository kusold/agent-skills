# simplified-technical

Write clear, unambiguous technical English based on [Simplified Technical English](https://www.asd-ste100.org/) (ASD-STE100), applied at roughly 80% strictness. Turns dense, jargon-heavy text into writing that reads like a good maintenance manual: direct, short, and hard to misread.

**Use when:**
- "Simplify this" / "Rewrite this for clarity"
- "Explain this like an aircraft manual"
- "Use STE / ASD-STE100 / simplified technical English"
- "De-jargon this"
- "Make this unambiguous / plain language"

## Why This Skill Exists

In October 2026, [Andrej Karpathy shared a writing tip on X](https://x.com/karpathy/status/2105819303471976479): ask your LLM to explain things in ASD-STE100, the controlled language originally developed for aerospace maintenance manuals. Its heavy constraints on writing style make output a lot more readable. Because the full specification is strict, he recommended softening the request to **"80% of the way to ASD-STE100"** — which is exactly what this skill encodes.

The 80% setting keeps the rules that pay for themselves (short sentences, simple tenses, active voice, one action per step, controlled word choice) and drops the ones that make text robotic (the full 900-word approved dictionary, strict one-word-one-part-of-speech enforcement, absolute bans that hurt natural flow).

## What Is Simplified Technical English?

ASD-STE100 is a controlled natural language with two parts:

1. **Writing rules** — 53 rules covering words, sentences, verbs, and procedures, with different requirements for procedural vs. descriptive text.
2. **A controlled dictionary** — roughly 900 approved words. Each word has one approved part of speech and one approved meaning. Non-approved words come with suggested approved alternatives.

It began in the late 1970s, when European airlines asked the aerospace industry association (AECMA, now ASD) to make aircraft maintenance documentation easier to understand — documentation written for readers with only a basic command of English, where ambiguity can be dangerous. The first Simplified English guide was released in 1986. It became an international specification in 2005 and an international standard with Issue 9 in 2025. See [Wikipedia: Simplified Technical English](https://en.wikipedia.org/wiki/Simplified_Technical_English) for more history.

The same properties that make it good for maintenance manuals make it good for LLM output and modern technical documentation: it removes hedging, cuts sentence sprawl, forces one instruction per step, and keeps domain terminology intact.

## What "80%" Means Here

| Kept (high value)                                              | Relaxed (hurts flow at full strictness)              |
| -------------------------------------------------------------- | ---------------------------------------------------- |
| Sentences ≤ 20 words (25 descriptive)                          | Full 900-word approved dictionary                    |
| One idea or instruction per sentence                           | Strict one-word-one-part-of-speech enforcement       |
| Simple tenses only; no progressive or perfect forms            | Absolute ban on "-ing" where it is a natural modifier |
| Active voice                                                   |                                                      |
| "must" for required, "can" for possible or permitted           |                                                      |
| Word substitution list for common jargon                       |                                                      |
| Numbered steps, one action per step                            |                                                      |
| Technical nouns and domain terms stay as-is                    |                                                      |
| No noun stacks longer than three words                         |                                                      |

For regulated domains (aviation, defense) that require certified ASD-STE100 compliance, use the [official specification](https://www.asd-ste100.org/) directly instead of this skill.

## Usage

The skill activates automatically when the agent detects a relevant request. The agent loads the full rules when the skill is active.

**Examples:**
```
Rewrite this README in simplified technical English
```
```
Explain how JWT auth works, 80% ASD-STE100
```
```
De-jargon this changelog entry
```

## Full Rule Reference

See [skills/simplified-technical/SKILL.md](../../skills/simplified-technical/SKILL.md) for the complete rules, substitution table, and before/after examples that the agent loads when this skill is active.

## Sources

- [Karpathy's X post on ASD-STE100](https://x.com/karpathy/status/2105819303471976479)
- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [Wikipedia: Simplified Technical English](https://en.wikipedia.org/wiki/Simplified_Technical_English)
