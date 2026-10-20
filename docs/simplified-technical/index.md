---
title: 'Simplified Technical English'
description: 'Write clear, unambiguous technical English based on ASD-STE100, applied at roughly 80% strictness.'
weight: 10
---

Write clear, unambiguous technical English based on [Simplified Technical English](https://www.asd-ste100.org/) (ASD-STE100), applied at roughly 80% strictness. Turns dense, jargon-heavy text into writing that reads like a good maintenance manual: direct, short, and hard to misread.

**Use when:**

- "Simplify this" / "Rewrite this for clarity"
- "Explain this like an aircraft manual"
- "Use STE / ASD-STE100 / simplified technical English"
- "De-jargon this"
- "Make this unambiguous / plain language"

## Why This Skill Exists

This skill adapts the writing principles of ASD-STE100 for everyday technical documentation. Here, **"80% strictness"** is an informal description of the approach, not a measured compliance score: favor short sentences, clear verbs, and consistent terminology while preserving meaning and natural flow.

The 80% setting keeps the rules that pay for themselves (short sentences, simple tenses, active voice, one action per step, controlled word choice) and drops the ones that make text robotic (the full 900-word approved dictionary, strict one-word-one-part-of-speech enforcement, absolute bans that hurt natural flow).

## What Is Simplified Technical English?

ASD-STE100 is a controlled natural language with two parts:

1. **Writing rules** — 53 rules covering words, sentences, verbs, and procedures, with different requirements for procedural vs. descriptive text.
2. **A controlled dictionary** — roughly 900 approved words. In general, each word has one approved part of speech and one approved meaning. Non-approved words come with suggested approved alternatives.

It began in the late 1970s, when European airlines asked the aerospace industry association (AECMA, now ASD) to make aircraft maintenance documentation easier to understand — documentation written for readers with only a basic command of English, where ambiguity can be dangerous. The first Simplified English guide was released in 1986. It became an international specification in 2005 and an international standard with Issue 9 in 2025. See the [official historical overview](https://www.asd-ste100.org/) for more history.

The same properties that make it good for maintenance manuals make it good for LLM output and modern technical documentation: it reduces needless complexity, favors one instruction per step, and keeps domain terminology intact. Rewrites preserve uncertainty, timing, and the distinction between recommendations and requirements.

## What "80%" Means Here

| Kept (high value)                                              | Relaxed (hurts flow at full strictness)              |
| -------------------------------------------------------------- | ---------------------------------------------------- |
| Sentences ≤ 20 words (25 descriptive)                          | Full 900-word approved dictionary                    |
| One idea or instruction per sentence                           | Strict one-word-one-part-of-speech enforcement       |
| Simple tenses when they preserve meaning                      | Progressive, perfect, and conditional forms when needed for precision |
| Active voice                                                   |                                                      |
| "must" for required, "should" for recommended, "can" for ability or permission | Context-dependent substitutions; uncertainty stays |
| Word substitution list for common jargon                       |                                                      |
| Numbered steps, one action per step                            |                                                      |
| Technical nouns and domain terms stay as-is                    |                                                      |
| No noun stacks longer than three words                         |                                                      |

For regulated domains (aviation, defense) that require full ASD-STE100 compliance, use the [official standard](https://www.asd-ste100.org/) and appropriate expert review. This skill does not verify compliance.

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration. The agent loads the full rules when the skill is active.

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

- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [ASD-STE100: how STE works](https://www.asd-ste100.org/about_STE.html)
