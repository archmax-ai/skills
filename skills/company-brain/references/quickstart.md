# Quickstart: setting up a brain

A guided interview in seven rounds. It matches Part 1 of `SKILL.md`: the answers fill the
house rules, then you build.

**How to run it**

- One round at a time, at most four questions per round. If you have a tool for asking
  structured questions, use it; otherwise number the questions and their options in plain
  text.
- Offer the options listed, always allow a free answer, and put the recommended option
  first.
- Skip a question when the files or earlier answers already settle it; say what you assumed.
- After each round, repeat the answers in one or two lines and note them for the house rules.
- The user can stop after any round. Write the foundation as soon as round 1 is done, so a
  stop still leaves a brain.

Open with one sentence: *"A brain is a shared set of notes on what you know — I'll ask a few
questions in seven short rounds, then build it with you area by area."*

---

## Round 1 — Scope

1. **Whose knowledge should the brain hold?**
   the whole company · a team or department · a product or project · my own work area
2. **What is it called, and who owns it?** *(free answer: a name for the brain and its
   self note, and the person who decides on its rules)*
3. **Where will it live?**
   a shared folder colleagues sync · a version-controlled repository · only on my machine ·
   not decided
4. **Who may read it?**
   everyone in the organisation · the team only · only me · it differs by topic
   → *differs by topic:* recommend separate brains per audience rather than mixed access.

**Then:** write the root `index.md`, `CHANGELOG.md`, the house rules' scope section and the
self note.

## Round 2 — Subject areas

1. **Which areas does your knowledge cover?** *(multiple choice; propose a starting set from
   the scope)*
   customers and contacts · people and team · products · services and pricing · strategy
   and positioning · competitors · market and trends · offers, invoices and contracts ·
   projects, talks and publications · funding · brand and templates · policies and playbooks
   · decisions · glossary

   Starting sets to propose:
   - sales or account team: customers, offers, competitors
   - product team: products, competitors, market and trends, decisions
   - consultant or small agency: customers, services and pricing, projects, offers
   - market intelligence: competitors, market and trends
   - whole company: three or four areas now, the rest later

2. **For each chosen area, explore it with the person** — two or three questions at a time:
   - What do you call this area? → folder name
   - What is one "thing" in it — a customer, a deal, a vendor, a document? → one concept
     per thing, and its `type`
   - What states does a thing go through? → `stage` values
   - What do people look up most often about it? → the sections of its notes
   - Do things in it have a history worth a timeline, or files that belong with them? →
     entity folder, timeline, attachments (see "Structure patterns" in `SKILL.md`)

   Propose the result as one line per area (*"`crm/` — one folder per organisation, types
   Customer, Contact, Timeline; stage lead → prospect → customer → former"*) and confirm.

**Then:** add the confirmed areas, types and stage values to the house rules. Create no
folders yet.

## Round 3 — Sources

1. **Where does this knowledge sit today?** *(multiple choice)*
   folders of documents · an email inbox · a contact list or exported customer data · slide
   decks and texts · websites · mostly in people's heads
2. **Where exactly?** *(free answer: paths, folder names, addresses)*
3. **Is anything in there that must stay out?**
   personnel files · financial details · customer-confidential material · credentials · no
4. **Which area should come first?** *(the chosen areas; recommend the one asked about most)*

**Then:** list the sources (do not read them yet) and show the ingestion plan: source → area →
action, plus what you will skip.

## Round 4 — People and trust

1. **Who can confirm content, per area?** *(free answer; only these people produce
   `verified` entries)*
2. **Is there anything that must never appear in documents for customers or the public?**
   internal code names · unapproved customer references · prices or terms · nothing
3. **Is there a current positioning or writing style that texts must follow?**
   yes, in a document I'll point to · yes, I'll describe it · not yet

**Then:** fill the house rules' verifiers and content-guardrails sections.

## Round 5 — Language and conventions

1. **Content language?** English · German · other
2. **File and folder names:** English lowercase with hyphens (recommended) · follow an
   existing convention
3. **Dates in the text:** `DD.MM.YYYY` · `YYYY-MM-DD`

**Then:** fill the naming section of the house rules.

## Round 6 — Routines

1. **Which jobs should run on their own?** *(multiple choice)*
   none yet (recommended to start) · brain mailbox · competitor monitoring · news and trend
   radar · customer watch · personal updates to colleagues · review sweep · deadline
   reminders
2. **For each chosen routine**, ask its settings from
   [routines.md](routines.md): owner, cadence, and —
   - mailbox: the address, who may send to it, whether senders get a confirmation;
   - monitoring and radar: sources to read, what counts as a competitor, how many trends;
   - personal updates: who receives them; offer to draft each person's interest profile;
   - deadline reminders: how far ahead.
3. Check the capabilities each needs. If one is missing, say so and record the routine as
   "later".

**Then:** fill the routines table of the house rules.

## Round 7 — Confirm and build

Show the plan in at most ten lines: scope, areas with folders and types, first area and its
sources, verifiers, language, routines. Ask: **"Shall I build it?"**
build now, starting with the first area · change something · stop here, the foundation is
enough for now

**Then:** follow Part 1 of `SKILL.md`. After each area, report briefly and ask: next area ·
confirm what was written · stop here.
