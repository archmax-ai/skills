# Writing a skill for this repository

A skill is one folder under `skills/`, named by its slug, holding a `SKILL.md` and any
references, scripts and assets it needs. `SKILL.md` is YAML frontmatter followed by guidance
written for the agent that will read it.

Two rules govern the **frontmatter** and are checked on every pull request: the
`description` is written for non-experts, and a `tools` key names the capabilities the skill
needs. Both apply to the frontmatter only. The body below it is written for the model that
will read it and may be as technical as the task demands.

## 1. Write the `description` for a non-expert

This rule is about the `description` field in the frontmatter, nothing else.

It does double duty. It is the only thing an agent sees before it decides to read the skill,
and it is the one line a person reads when deciding whether to install the skill from a list.
That person is not a developer and does not know the technology the skill is built on.

So say what the skill lets someone *do*, in the words they would use, and then say when to
reach for it. A reader who has never heard of the file format, protocol or library behind the
skill should still understand what it is for.

- Name the everyday thing, not its internals: "Word, Excel and PowerPoint files", not
  "OOXML packages"; "invoices", not "UBL 2.1 documents".
- Mention the format's familiar name or extension only as a clarifier, after the plain words.
- No jargon, no acronyms a layperson would not recognise, no implementation detail: not
  "unpacks the zip container and edits its XML parts". How the skill works belongs in the
  body.
- Keep it to one or two sentences, and end with the trigger — the moment the agent should
  read it. The trigger sentence is what makes the skill get chosen at the right time.
- Write it as a statement about the skill, not a command to the reader.

```yaml
# Good — a person understands it, and the agent knows when to use it
description: Fill in and edit Word, Excel and PowerPoint files — letters, spreadsheets and
  slide decks — starting from a template. Read this before creating or changing any DOCX,
  XLSX or PPTX file.

# Bad — correct, but only to someone who already knows the format
description: Manipulate OOXML packages by unzipping the container, patching the XML parts
  and rezipping.
```

## 2. Declare the tools the skill needs

Every `SKILL.md` carries a `tools` key: a list of the capabilities an agent must have to
follow the skill. It lets a person tell before installing whether their agent can run the
skill at all, and it lets the agent check itself before it starts.

```yaml
---
name: Microsoft Office Documents
description: ...
tools:
  - Unpack a file archive into a folder, and pack a folder back into one file
  - List, read, search and edit files as text
  - Copy or move a file without opening it (only for documents with pictures)
  - View a document's text and tables
  - Send or store the finished file
---
```

Rules for the list:

- **Describe capabilities, never tool names.** Write "a tool that unpacks a zip archive into
  a folder", not `unzip_archive`, `Bash` or any one agent's tool name. Tool names differ
  between agents and change over time; the agent reading the skill already sees its own
  tools' names and descriptions and can match them to a capability.
- **Keep each entry to one short line.** It is frontmatter, so it is read by the same person
  who reads the description — plain words, no tool syntax. The detail — what the capability
  is used for, what its limits are — goes in the body.
- **List only what the skill genuinely cannot do without.** A skill that needs nothing beyond
  reading and writing files says so; do not pad the list.
- **Mark what is optional** in the entry itself, for example "(only for documents with
  pictures)".
- **If it must be executed, ship it.** Anything the agent has to run belongs in the skill's
  `scripts/` folder; the `tools` list says the agent needs to be able to run a script, not
  that some external program exists.

Repeat the list in the body as a short "What you need" section at the top of `SKILL.md`, with
one or two sentences per capability, and tell the agent to say which capability is missing
and stop rather than improvise.

## The body

The rules above stop at the frontmatter. The body is read only by the model that runs the
skill, so write it for that reader: technical terms, file formats, XML, exact paths and
protocol detail all belong here, at whatever depth the task needs. It does not have to be
understandable to a non-expert, and simplifying it at the cost of precision makes the skill
worse.

- Write for the agent that will read it, not for a human reviewer.
- State the rules that keep a task from going wrong, and the order of steps that works.
- Leave out anything the agent's own tool descriptions already say.
- Refer to files by path relative to the working directory. Do not name folders that only
  exist on one platform.
- Nothing in the bundle runs except files under `scripts/`.

## Staying platform-neutral

This repository is not tied to a particular agent, product or deployment. Do not name one in
a skill, a description or a reference — no product names, no host-specific environment
variables, no tool names from one agent's toolset. A skill should read the same whether it is
installed into a hosted platform, a local agent or a CI job.

## Checklist before opening a pull request

- [ ] Folder is `skills/<slug>/` with a lowercase-hyphen slug and no symbolic links.
- [ ] `SKILL.md` has `name`, `description` and `tools`.
- [ ] The frontmatter `description` is understandable to someone who does not know the
      underlying technology, and ends with when to use the skill. (The body has no such
      constraint.)
- [ ] `tools` lists capabilities, not tool names, and the body repeats them under "What you
      need".
- [ ] No product, platform or agent names anywhere in the bundle.
- [ ] Everything executable lives under `scripts/`; the bundle is small.
