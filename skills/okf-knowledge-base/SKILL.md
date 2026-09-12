---
name: OKF Knowledge Base
description: Read, write and reorganise a shared knowledge base — a folder of plain notes, one per topic, each with a short labelled header and links to related notes, that people and software can both use. Read this before adding, editing, moving or deleting notes in a knowledge base that follows the Open Knowledge Format (OKF).
tools:
  - List, read, search, create and edit files as text
  - Move or rename a file (only when reorganising the folders)
  - Find out the current date and time
  - Run a script that ships with this skill (only for the check at the end)
  - Fetch a web page (only when a note records material from the web)
---

# OKF knowledge base

A knowledge base in this format — a **bundle** — is a directory tree of markdown files. One
file is one **concept**: a table, a metric, a playbook, a policy, an API, an idea. Each file
is YAML frontmatter followed by a markdown body, and files link to each other with ordinary
markdown links, so the bundle is a graph, not just a tree.

The format is deliberately thin. Only one frontmatter key is required (`type`), a consumer
must not reject a bundle for anything else, and nothing validates you. That means almost
every mistake you can make here is a *silent* one: a link that points nowhere, an index that
no longer matches its directory, a claim with no source, a folder nobody would think to open.
The rules below are what keeps a bundle usable after a few hundred edits.

## What you need

This skill assumes the capabilities listed in its frontmatter. Check that you have each
before you start; if one is missing, say which and stop rather than improvising.

- **Read and edit files as text** — list a directory, read a file, search the tree for a
  string, write a new file, and replace exact strings in an existing one. Searching the whole
  bundle is not optional: it is how you find the concepts to link to and the links to fix.
- **Move or rename a file** — needed only when you reorganise. A concept's identity *is* its
  path, so a move is a breaking change and must be followed by a link fix (see "Moving a
  concept").
- **The current date and time** — every timestamp you write is an ISO 8601 instant with a UTC
  offset (`2026-09-12T14:30:00Z`). Never guess it and never copy a neighbouring file's.
- **Run a script** — `scripts/check_bundle.py` checks the bundle before you finish. If you
  cannot run scripts, do the checks by searching instead; the script's output describes each
  one.
- **Fetch a web page** — only when a concept records material from the web. Record only
  sources you actually read.

## Core rules

1. **One concept per file, and `type` in every one.** A concept file with no frontmatter, or
   with an empty `type`, breaks the format. Everything else is optional — but write `title`
   and `description` too: index entries, search results and previews are built from them.
2. **`index.md` and `log.md` are reserved.** They are never concept documents. Never give a
   concept one of those names, and never put frontmatter in an `index.md` (a bundle-root
   `okf_version` is the single exception).
3. **Never invent a second metadata scheme.** If you need a field the format does not name,
   add a plain frontmatter key. Do not put metadata in the body, in a file name, in a
   sidecar file, or in a folder name.
4. **Say who wrote it, and never claim a check that did not happen.** `generated.by` is you
   (`<producer>/<version>`). Only write a `verified` entry for a person when that person
   actually confirmed the content in this session (see "Provenance and trust").
5. **Every edit that changes the tree changes three other things.** Adding, moving or
   removing a concept means: fix the links that pointed at it, update the `index.md` of every
   directory involved, and add a `log.md` entry. Nothing does this for you.
6. **Prefer deprecating to deleting.** Other concepts link to a file; links that point
   nowhere are legal and so nothing will tell you that you broke one. Set
   `status: deprecated`, say in the body what replaces it, and keep the file.
7. **Run the check before you finish.** `python3 scripts/check_bundle.py <bundle-dir>` —
   errors mean the bundle is no longer conformant.

## Reading a bundle

Read top-down, not by reading every file:

1. Read the bundle-root `index.md`. It lists the directories and what is in them, and is what
   the format calls progressive disclosure — it exists so you do not have to open everything.
2. Read the `index.md` of the directory you need, then the concepts it names.
3. When there is no index, list the tree and search frontmatter instead: `type:` values tell
   you what kinds of concept exist, `tags:` values cut across directories.
4. Read `log.md` when you need to know what recently changed or why something was retired.

Before answering from a concept, look at its `status` (`deprecated` means do not use it for
new work), its `stale_after` (past that instant the content is stale), and whether it carries
a `verified` entry at all. Unverified content is still usable — say that it is unverified.

## Writing a concept

The smallest conformant file is frontmatter with `type` and a body. Write this instead:

```markdown
---
type: Metric
title: Weekly active users
description: Distinct users with at least one session in a calendar week.
tags: [product, engagement]
generated: { by: <producer>/<version>, at: 2026-09-12T14:30:00Z }
sources:
  - id: analytics-handbook
    resource: https://wiki.example/analytics/handbook
    title: Analytics handbook
---

# Definition

A user counts as active in a week when they have at least one session, per the analytics
handbook.[^analytics-handbook] Sessions come from the [events table](../tables/events.md).

[^analytics-handbook]: Analytics handbook
```

- `type` is a short, self-explanatory string. Reuse a value the bundle already uses — search
  for `^type:` before inventing a new one. Nothing registers types centrally, so two spellings
  of the same kind (`Playbook` and `Runbook`) split the bundle silently.
- `description` is **one sentence**. It is copied verbatim into `index.md` entries.
- `resource` is the URI of the thing the concept describes, when it describes a real asset.
  Omit it for abstract concepts.
- Favour structural markdown — headings, tables, fenced code — over prose paragraphs. The
  conventional headings are `# Schema`, `# Examples` and `# Computation`.
- Attribute a specific claim with a footnote whose label is a `sources[].id`, as above. Do not
  write a `# Citations` section; provenance lives in frontmatter.

The full field reference, including attested computations, is in
[references/frontmatter.md](references/frontmatter.md).

### Linking

Links are how the bundle becomes a graph, so link a concept the first time the prose mentions
it — once per section is enough, never from headings or code blocks. The link asserts *some*
relationship; the surrounding prose says which.

Two forms exist, and a bundle should use one throughout:

- **Relative** (`../tables/orders.md`) renders correctly when the bundle is browsed as plain
  files or on a git host. This is the safer default.
- **Bundle-absolute** (`/tables/orders.md`, from the bundle root) survives a file being moved
  within its directory, but does not resolve in a plain file browser.

Match whichever the bundle already uses — search for `](/` to find out. Never link to a file
you have not confirmed exists; broken links are legal and therefore invisible.

## Folders: when to create one, and when not to

The format says nothing about directory structure, so this is where bundles rot. Directory
structure is a navigation aid for readers, and every folder costs every reader a hop.

**Start flat.** A new bundle is concept files in the root plus an `index.md`. Add structure
when the flat list stops being readable, not before:

| Concepts in the bundle | Structure |
|------------------------|-----------|
| under ~12 | flat root, one `index.md` |
| ~12 to ~40 | one level of directories, each with an `index.md` |
| over ~40 | two levels; a third only for a genuinely deep subtree |

**Create a subdirectory only when all three hold:**

1. **Five or more concepts belong to it already.** Not "will one day" — group concepts when
   they exist, not in anticipation.
2. **A reader would think of the group's name before the concept's name.** The group has to
   be how people ask for things, not how you happened to classify them.
3. **You can write its one-line description** for the parent's `index.md`. If you cannot say
   what belongs in it in one line, the grouping is not real.

**Never create:**

- a directory holding one concept;
- a directory created for symmetry, because a sibling exists;
- a pass-through directory that holds only another directory;
- a directory named after an internal team or system that readers do not use;
- anything more than three levels below the bundle root.

**One axis per level.** Pick how a level divides and hold to it:

- **By kind of concept** — `tables/`, `metrics/`, `playbooks/`, `policies/`. Use this at the
  top when the bundle covers one domain.
- **By domain or owner** — `sales/`, `finance/`, `support/`. Use this at the top when the
  bundle spans teams, and each subtree has a different owner and its own lifecycle. Divide by
  kind *inside* each domain.

Never mix the two in one directory: a `tables/` folder sitting next to a `finance/` folder
forces every reader to guess which parent a concept lives under, and every writer to make the
same guess again.

**Folders are for ownership and lifecycle; tags are for everything else.** Concepts that are
maintained, regenerated, verified, deprecated or deleted together belong in a directory
together. A cross-cutting grouping — everything about Q3, everything touching revenue — is
`tags` plus links. A consumer can synthesise a tag view by scanning frontmatter; it cannot
synthesise ownership.

**Do not mirror an external hierarchy** — a warehouse's project/dataset/table nesting, a
department's org chart — unless readers actually navigate that way. Record the external
identity in `resource` instead, where it belongs.

**`references/`** is the conventional name for material the bundle mirrors rather than
authors: external documents, run instructions, executable checks, join notes. Existing
bundles also keep derived reference concepts there. Anything else in the tree may point into
it.

### Splitting a directory that grew

1. Create the directory and write its `index.md` first, so nothing is ever unlisted.
2. Move the files.
3. Search the whole bundle for each old path and fix every link. This is the step that gets
   skipped and the one that breaks the graph.
4. Update the parent `index.md` to list the new directory, and remove the moved entries.
5. Add a `log.md` entry naming what moved and why.

### When to split one concept into two files

Split when the parts have **independent lifecycles**: separately verified, separately stale,
separately owned, or useful to different readers. Keep them in one file when a reader would
ask about them as one thing. A narrative concept that links to several precise ones — an
overview linking to each figure it discusses — is the normal shape, not a compromise.

### File names

Lowercase letters, digits and hyphens; `.md`; no spaces. Mirror the underlying asset's own
identifier when there is one (`orders.md` for a table named `orders`), otherwise name the
concept, not its category — `weekly-active-users.md`, not `metric-3.md`. Directory names are
plural for collections (`tables/`, `metrics/`); file names are singular.

Names are identity, so treat a rename as a breaking change: see "Moving a concept".

## index.md

An `index.md` lists what is in its directory, so a reader can see the group without opening
anything. Every directory with five or more concepts should have one; a directory with
subdirectories should always have one.

No frontmatter. One or more sections, each a heading and a bulleted list of links with the
linked concept's own `description` after a dash:

```markdown
# Tables

* [Orders](orders.md) - One row per completed customer order across all channels.
* [Customers](customers.md) - One row per customer account, current state only.

# Subdirectories

* [metrics](metrics/index.md) - Business definitions of the headline numbers.
```

Keep entries in the same link style as the rest of the bundle. When you add, move or remove a
concept, update the index in the same edit — an index that disagrees with its directory is
worse than no index, because readers stop opening the files it omits.

## log.md

A `log.md` may sit at any level and records the history of that scope. Newest first, one
`## YYYY-MM-DD` heading per day, ISO dates only:

```markdown
# Bundle history

## 2026-09-12

- **Update**: Rewrote [weekly active users](/metrics/weekly-active-users.md) after the
  session definition changed; `stale_after` moved to 2027-01-01.
- **Deprecation**: [Legacy margin](/metrics/gross-margin-legacy.md) retired in favour of
  [gross margin](/metrics/gross-margin.md).

## 2026-08-30

- **Creation**: Added the `policies/` directory with the three finance policies it mirrors.
```

The bold leading word (`**Update**`, `**Creation**`, `**Deprecation**`, `**Verified**`) is a
convention, not a requirement. Write entries a person can read a year later: what changed and
why, not "updated file".

## Editing an existing concept

1. Read the file before you change it, and refine it rather than rewriting it — the existing
   wording may be what someone verified.
2. Update `generated` to yourself and the current time whenever the content meaningfully
   changes.
3. **Leave existing `verified` entries alone.** They are dated events, not a badge. A reader
   comparing `verified[].at` with `generated.at` can see the check predates your change; that
   is the design. Deleting them destroys that signal, and re-dating them is a false claim.
4. Revisit `stale_after` and `status` while you are in the file.
5. If the concept has become wrong rather than out of date, say so in the body — do not
   quietly correct a number that reports and dashboards may have used.

### Moving a concept

The path is the concept's identity, so a move breaks every link to it and no tool will report
it. Search the bundle for the old file name, fix each link, update both `index.md` files, and
log the move. When the concept is widely linked or externally referenced, leave the old file
in place with `status: deprecated` and a one-line body pointing at the new location instead of
moving it silently.

## Provenance and trust

These fields are what make an agent-maintained bundle trustable, so they are the ones where a
convenient lie does the most damage.

- **`generated: { by, at }`** — who produced the current content and when. `by` is an actor:
  `<producer>/<version>` for a tool or agent, `human:<id>` for a person, `process:<id>` for an
  automated process. Content you wrote is yours: never label it `human:`.
- **`verified: [{ by, at }]`** — who has *confirmed* the content against its sources. A
  consumer derives a trust tier from it: no `verified` is unverified, non-human verifiers are
  machine-confirmed, a `human:` verifier is human-reviewed. Add a `human:` entry only when a
  person has actually confirmed it in this session. If nobody has checked your work, the
  correct state is no `verified` key at all.
- **`sources`** — the materials the concept derives from, each with a `resource` and, when the
  body cites it, a stable `id`. Record only sources you actually consulted; never invent a
  URL to make a claim look grounded. Optional credibility signals (`author`, `usage_count`,
  `last_modified`, and a `usage_window` sibling) go on the entry when you know them.
- **`status`** — `draft` while incomplete, `stable` (the default) when ready, `deprecated`
  when retired. Use `draft` rather than leaving something half-written that reads as current.
- **`stale_after`** — the absolute instant the content should stop being trusted. Set it on
  anything that tracks a policy, a schema or a figure that will change.

## Attested computations

A concept of `type: Attested Computation` carries a *sanctioned* way to compute a value so a
consumer can confirm the blessed computation ran rather than an improvised one. When you meet
one:

- **Never author or edit the computation.** You may supply values for the declared
  `parameters` and nothing else. Rewriting the SQL, swapping the referenced file, or
  "fixing" it inline defeats the entire mechanism.
- A concept that needs the value links to the computation; it does not copy it.
- Creating one is a deliberate act — `runtime`, `parameters`, the computation itself, and the
  `executor`/`attester` pair. See [references/frontmatter.md](references/frontmatter.md)
  before writing one, and prefer linking an existing computation to writing a second one for
  the same figure.

## Before you finish

Run the check over the bundle, giving it the bundle's root directory:

```
python3 scripts/check_bundle.py <bundle-dir>
```

It reports three levels: **ERROR** breaks the format and must be fixed; **WARN** is legal but
almost always a mistake (broken links, non-ISO timestamps, an index that omits a file, a
passed `stale_after`); **NOTE** is a structure or naming habit worth fixing while you are
there. It exits non-zero only on errors, and checks frontmatter more precisely when a YAML
parser is importable — the output line says which mode it ran in.

Then confirm by hand what the script cannot judge: that each new `description` reads as one
useful sentence, that every claim you added is either sourced or visibly unverified, and that
the `log.md` entry says why, not just what.
