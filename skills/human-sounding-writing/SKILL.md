---
name: Human-Sounding Writing
description: Write text that reads as if a person wrote it, with sentences of different lengths, plain words, no dashes standing in for commas and no stock phrases. Read this before writing anything a person will read, such as an email, a reply, a summary or a post, and check the draft with the skill's script before sending it.
tools:
  - Read and write text
  - Run a script that comes with the skill (to check a draft)
icon: PenLine
color: teal
---

# Human-Sounding Writing

Text written by a language model has a sound people learn to spot within a sentence or two. Every
sentence is about as long as the last, a dash turns up in every other line, the same grand words
keep coming back, and a tidy summary closes it. None of it is wrong. Together, though, it reads as
nobody in particular, and this skill is how to write so the reader hears a person.

## What you need

- **Read and write text.** You draft, reread and revise.
- **Run a script that comes with the skill.** `scripts/check-prose.js` measures a draft's
  sentence lengths and finds its dashes. If you cannot run it, say so, then check the draft by
  hand against the rules below rather than skipping the check.

## The rules

1. **Vary the length of your sentences**: mix short ones with long ones. A short sentence lands a
   point. A longer one can carry a reason, a condition and an example without strain, as long as
   it says one thing. Three sentences in a row of about the same length is a pattern the reader
   notices before they notice anything you said.
2. **Keep most sentences under 25 words**, and break any over 30 unless its rhythm is the point.
3. **Use no em dashes** (`—`). Where you reach for one, use a comma, a colon, parentheses or a
   full stop and a new sentence. Do not swap in an en dash (`–`) or a double hyphen (`--`). A
   hyphen inside a word (well-known) is fine.
4. **Say it plainly.** Prefer the everyday word: use, not leverage; help, not facilitate; show,
   not showcase. Leave out words that announce importance instead of showing it: crucial,
   pivotal, robust, seamless, delve, tapestry, landscape, realm, navigate, unlock, elevate.
5. **Start with the answer.** Do not restate the question, thank the reader for asking, or open
   with "Great question". Do not end with "In conclusion", "Overall" or a summary of what you just
   said. Stop when you are done.
6. **Be specific.** A number, a name, a date or an example says more than an adjective. "Saves
   about two hours a week" beats "significantly improves efficiency".
7. **Do not list in threes by reflex.** Three adjectives, three benefits and three examples in
   every paragraph is a tell. Use as many as there are: often one, sometimes two.
8. **Write as you would speak to the reader.** Use contractions where the register allows (it's,
   you'll), the active voice, and "you" and "we" when you mean them. Hedge once, where there is
   real doubt, not in every sentence.
9. **Use formatting only for structure**: bullets for a real list, headings for a long document,
   and bold for the one thing that must not be missed. Keep a short answer in plain prose.

## Checking a draft

Run `scripts/check-prose.js` with the draft as `text`. It returns:

- `verdict`: `ok`, or `revise` with the reasons in `advice`;
- `sentences`, `words`, `meanLength` and `spread` (the standard deviation of sentence length in
  words; under 5 reads flat, 7 and over reads natural for most prose);
- `longSentences`: each sentence over 30 words, with its length and its first words;
- `sameLengthRuns`: each run of three or more sentences within two words of each other;
- `dashes`: each em dash, en dash used as a dash, and double hyphen, with its line and context.

Revise until the verdict is `ok`, then read the draft once more as the person receiving it would.
The script measures rhythm and punctuation only; rules 4 to 9 are yours to check.

Outside an agent, run it on a file:

```sh
node scripts/check-prose.js draft.md
```
