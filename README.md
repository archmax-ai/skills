# Skills

A registry of agent skills. Each skill is a folder holding a `SKILL.md` and whatever
references, scripts and assets it needs. A platform that offers skills to its users clones
this repository and copies a skill into an environment on request; after that copy the
environment owns the files and nothing at run time reads this repository.

The repository is not tied to any one platform or agent. A skill here describes a task and
the capabilities it needs — not the tool names of whichever agent ends up reading it.

## Layout

```
skills/<slug>/SKILL.md      # required: YAML frontmatter, then the guidance
skills/<slug>/references/   # optional: documents the skill tells the agent to read
skills/<slug>/scripts/      # optional: runtime scripts the agent may execute
skills/<slug>/assets/       # optional: data files the skill refers to
```

One level, no categories: every direct child of `skills/` that holds a `SKILL.md` is one
skill, and its **directory name is the slug** — the identifier the skill is granted by and
installs under. Slugs are lowercase letters, digits and hyphens (`refund-policy`,
`microsoft-office-documents`). A directory without a `SKILL.md`, with any other name shape, or
containing a symbolic link is not a skill.

Every regular file beneath a skill's directory is part of its bundle and is copied on
install. Keep bundles small: a host may refuse an oversized file, and a skill's whole text is
read by the model once the skill is chosen.

## Frontmatter

```yaml
---
name: Microsoft Office Documents
description: Fill in and edit Word, Excel and PowerPoint files — letters, spreadsheets and slide decks — starting from an existing template. Read this before creating or changing any DOCX, XLSX or PPTX file.
tools:
  - Unpack a file archive into a folder, and pack a folder back into one file
  - List, read, search and edit files as text
  - Copy or move a file without opening it (only for documents with pictures)
  - View a document's text and tables
  - Send or store the finished file
---
```

- `name` — what a person and the agent see in a list of skills.
- `description` — the only thing the agent sees before choosing the skill, and the line a
  person reads when deciding whether to install it. Write it for someone who does not know
  the underlying technology.
- `tools` — the capabilities the skill needs, so a person can tell before installing whether
  their agent can follow it.

The plain-language rule covers these frontmatter fields only. The guidance below the
frontmatter is read by the model that runs the skill and is as technical as the task needs.

Other keys are preserved on install; a host may add its own `metadata` recording where a
skill was copied from.

## Contributing

Open a pull request adding `skills/<slug>/`. [AGENTS.md](AGENTS.md) is the contract every
skill in this repository follows — read it before writing one.

Licensed under the MIT License (see `LICENSE`).
