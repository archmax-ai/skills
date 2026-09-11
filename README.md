# Pangea skills

Skills the Pangea platform offers from its **Browse skills** dialog. A deployment names this
repository in its registries document (`PANGEA_SKILL_REGISTRIES`), clones it when the API
starts, and lets an owner copy any skill here into an environment's `skills/` folder. After
that copy the environment owns the files: they are edited, published and promoted like a
skill written by hand, and nothing at run time reads this repository.

## Layout

```
skills/<slug>/SKILL.md      # required: YAML frontmatter with `name` and `description`, then the guidance
skills/<slug>/references/   # optional: documents the skill tells the agent to read
skills/<slug>/scripts/      # optional: runtime scripts the agent may execute with pangea_run
skills/<slug>/assets/       # optional: data files the skill refers to
```

One level, no categories: every direct child of `skills/` that holds a `SKILL.md` is one
skill, and its **directory name is the slug** — the identifier a workflow grants it by in
`skills.allow` / `skills.allow_always` and the name it installs under. Slugs are lowercase
letters, digits and hyphens (`refund-policy`, `microsoft-office-documents`). A directory without a
`SKILL.md`, with any other name shape, or containing a symbolic link is not offered.

Every regular file beneath a skill's directory is part of its bundle and is copied on
install. Keep bundles small: the platform refuses a file above its shared 20 MiB cap, and
a skill's whole text is read by the model once the skill is chosen.

## Frontmatter

```yaml
---
name: Microsoft Office Documents
description: Fill and edit Microsoft Office documents — Word DOCX, Excel XLSX and PowerPoint PPTX — from a template. Read this before creating or changing any DOCX, XLSX or PPTX file.
---
```

`name` is what the owner and the agent see; `description` is **all the agent sees before
choosing the skill**, so say what it covers and the moments that should trigger it. Other
keys are preserved on install; the platform adds a `metadata` mapping recording the registry,
the slug and the commit a skill was copied from.

## Contributing

Open a pull request adding `skills/<slug>/`. Write for the agent that will read it. Describe
the **capabilities** a skill needs — "a tool that unpacks a zip container into a folder" — and
how to use them, rather than naming platform tools: tool names differ between agents and
change over time, and the agent reading the skill already sees its own tools' names and
descriptions. Open with a short "What you need" list so the agent can tell at once whether it
can follow the skill, state the rules that keep a task from going wrong, and leave out anything
the tools' own descriptions already say. Anything the agent must be able to execute goes under
`scripts/`; nothing else in a bundle runs.

Licensed under the MIT License (see `LICENSE`).
