---
name: simplified-technical
description: Write or rewrite text in Simplified Technical English at roughly 80% ASD-STE100 strictness. Use when the user asks to "simplify this", "rewrite for clarity", "explain like an aircraft manual", "use STE / ASD-STE100 / simplified technical English", "de-jargon this", "make this unambiguous", or wants plain-language technical documentation. Not for creative or marketing copy.
metadata:
  author: mikekusold
  version: "1.1.0"
---

# Simplified Technical English

Write technical English that is hard to misread. Apply the high-value rules of [ASD-STE100](https://www.asd-ste100.org/) — the aerospace controlled-language specification — at about 80% strictness. Write for a reader with basic English and no context. When a rule fights clarity or natural flow, clarity wins.

## Preserve Meaning

A rewrite changes style, not facts.

- Keep every fact, condition, number, and scope qualifier from the source.
- Never add a cause, a frequency, or a mechanism that the source did not state.
- If a shorter phrasing would lose precision, keep the longer phrasing. Say which phrase you kept and why.

## Words

- Use the simplest word that is correct: "use" not "utilize", "show" not "demonstrate".
- No phrasal verbs ("take off", "spin up", "reach out"). Use one plain verb: "remove", "start", "contact".
- Use the verb, not a noun made from the verb. Write "analyze the log", not "perform an analysis of the log".
- Cut marketing adjectives ("seamless", "robust", "cutting-edge"). Delete the adjective, or replace it with the measurement that earns the claim.
- Pick one meaning per word and keep it. If "enter" means "type into a field", do not also use it to mean "go into".
- Keep technical nouns and domain terms exactly as they are ("JWT", "Kubernetes pod", "cache invalidation"). Do not simplify terminology the reader needs.
- Do not drop articles (a, an, the) to save space.
- No noun stacks longer than three words. Rewrite "database connection pool max size setting" as "the max size setting for the database connection pool".

## Sentences

- Keep sentences to 20 words or fewer (25 for descriptive text).
- One idea or one instruction per sentence.
- Do not use semicolons. Split the sentence into two sentences.
- Paragraphs: one topic, six sentences maximum.
- Put the main point first.

## Verbs

- Use only simple forms: imperative, simple present, simple past, simple future ("will").
  - Not "The service is restarting" → "The service restarts"
  - Not "The job has completed" → "The job is complete"
  - Not "would have been triggered" → "the job triggers"
- Write in the active voice. Use passive only when the actor is unknown or irrelevant.
- "must" = required. "can" = possible or permitted. Do not use "should", "shall", or "may" for obligation or permission.
- Keep hedges that report uncertainty. A hedge is content, not style. "The request may have failed" must not become "The request failed". When the tense rules conflict with a hedge, keep the hedge.
- Remove stacked hedges: "this may potentially help" → "this may help".
- No "-ing" verb forms. Use -ing only in technical nouns and modifiers ("the cooling fan"). "Close the valve by turning the handle" → "Turn the handle to close the valve."

## Procedures

- Write steps as a numbered list. One action per step.
- Start each step with an imperative verb ("Install...", "Check...", "Remove...").
- Put warnings before the step they apply to, prefixed with "WARNING:" or "CAUTION:".
- When a step has a condition, put the condition first: "If the indicator is red, stop the pump."

## Word Substitutions

Replace common complex words:

| Instead of            | Use            |
| --------------------- | -------------- |
| additional            | more           |
| approximately         | about          |
| assist, facilitate    | help           |
| attempt               | try            |
| commence, initiate    | start          |
| concerning, regarding | about          |
| demonstrate           | show           |
| determine             | decide, find   |
| ensure                | make sure      |
| insufficient          | not enough     |
| leverage, utilize     | use            |
| may (permission)      | can            |
| obtain                | get            |
| prior to              | before         |
| provide               | give           |
| purchase              | buy            |
| require               | need           |
| should, shall         | must           |
| subsequent to         | after          |
| terminate             | stop           |
| transmit              | send           |
| verify                | check          |

## Examples

**Description — before:**

> The authentication service utilizes JSON Web Tokens in order to facilitate stateless verification of user identity, with expired tokens being automatically refreshed.

**After:**

> The authentication service uses JSON Web Tokens (JWT). A JWT contains the identity of the user. The service checks this identity and does not need a session store. The service gets a new token automatically before the old token expires.

**Procedure — before:**

> Before initiating the migration, you should ensure that a backup has been created and that all active connections are terminated.

**After:**

> WARNING: If you do not make a backup first, you can lose data.
>
> 1. Back up the database.
> 2. Stop the application. This closes all open connections.
> 3. Start the migration.

**Status message — before:**

> The deployment may have failed due to a possible timeout while the service was starting, which could be caused by insufficient resources.

**After:**

> The deployment may have failed. A timeout may have stopped the service during startup. A timeout can occur when the cluster does not have enough resources. Check the resource limits of the cluster.

Both hedges stay. A rewrite that says "The deployment failed" makes a different claim than the source.

## Stay at 80%

The goal is clarity, not compliance. Do not:

- Replace a precise technical term with vague simple words. "Authenticate" stays; do not write "make an identity check".
- Break every sentence into robotic fragments. A short sentence with a conjunction reads better than three choppy ones.
- Cut useful context or caveats to shorten text. Move them to a note instead.

When machines parse the text (tool descriptions, error messages, inter-agent instructions), apply the rules fully. A wrong reading has a real cost. When the full specification matters (aviation, defense, regulated documentation), say so and follow ASD-STE100 directly.

## Output

- Give the rewritten text only. Do not add a preamble, a change summary, or an offer to explain more.
- When you keep a longer phrasing to preserve precision, add one line after the text: "Kept as-is: <phrase> (<reason>)".
- When the user asks what changed ("show the diff", "what did you change"), give a table of rule, before, and after.
- When the input already complies, say so. Do not force changes onto clean text.
