---
name: OOXML documents
description: Fill and edit Word (.docx), Excel (.xlsx) and PowerPoint (.pptx) documents from a template by unpacking the container, editing its XML parts and packing it again. Read this before creating or changing any Office document.
---

# OOXML documents

An Office document is a zip container of XML parts. You never write the binary; you unpack
the container, edit the parts as text, and pack it again.

## What you need

This skill assumes four capabilities. Check that you have each before you start; if one is
missing, say which and stop rather than improvising.

- **Unpack a container** — a tool that takes a file you hold and extracts every entry into a
  folder, preserving the entry paths (`word/document.xml`, `[Content_Types].xml`). Office
  files are zips, so any tool that unpacks a `.zip` unpacks a `.docx`.
- **Pack a folder** — a tool that zips a folder back into one file, keeping paths relative to
  the folder and the file extension you give the result. This is what turns the edited folder
  into a valid `.docx`, `.xlsx` or `.pptx`.
- **Read and edit files as text** — list a folder, read a file, search files for a string, and
  replace one exact string with another in a file. Writing a whole new file is needed only
  when adding a part, such as a new sheet.
- **Render a document as text** — a tool that shows a document's prose and tables as markdown.
  Use it to read; it never edits.

Files are referred to by the paths your file tools report, relative to your working folder.
Never paste a file's bytes into a tool argument.

## Core rules

1. **Never write a `.docx`, `.xlsx` or `.pptx` from scratch.** Derive it from a template: a
   document attached to this conversation, one in a folder you were given, or one you fetched
   from a link. List and search your folders before asking. Raw OOXML written by hand yields
   missing styles and files Office refuses to open. If no template exists, ask for one — and
   if nobody is watching this session, ask through the channel the request came from.
2. **Read as text, edit as parts.** Render the whole document to see what it says. Change it by
   unpacking, editing parts, packing.
3. **Nothing checks your XML.** A part that is no longer well-formed produces a document Office
   rejects, and no tool warns you. Keep every edit inside whole elements and escape text (see
   "XML must stay well-formed").
4. **Deliver with a tool.** A packed document in your working folder reaches nobody by itself:
   attach it with the tool that sends messages, hand it to the tool that stores or forwards
   files, or create a download link when a person or system needs one.

## Workflow: unpack → edit → pack

1. Unpack the template into a folder of its own, one folder per document (`doc/`, `xl/`), so
   two documents never mix parts.
2. List the folder to see the parts; search it for your placeholders (for example `[[`) to learn
   which part holds each one — a date may sit in the body and in a header.
3. Read the part you will change to see its actual XML around the placeholder.
4. Replace strings, one region per edit.
5. Pack the folder into a file whose name carries the right extension, then deliver it.

Notes:

- Do not add or remove files in the folder unless you also update `[Content_Types].xml` and
  the relationship parts (see "Add a new sheet").
- Address `[Content_Types].xml` by its exact path with read and edit. Do not use a glob pattern
  for it: the brackets are a character class in glob syntax.
- Word and Excel emit their XML as one very long line. Search first to locate the region, then
  replace with an `old` string that is unique and short. Replace one region per edit rather than
  rewriting a whole `document.xml` or `sheetN.xml`; a rewritten part is a part you had to
  reproduce perfectly.

## Reading a document

1. Render the container as markdown to confirm it is the right file and see its shape.
2. Unpack it and list the folder to see the parts.
3. Read the part you will change to see the raw XML.

Rendering works on the container; on an unpacked XML part use the plain file reader.

## Editing

Edit by exact-string replacement: an `old` string that occurs once, a `new` string that
replaces it. Replace all occurrences only when every occurrence really is the same edit.

### XML must stay well-formed

The usual ways an edit breaks a part:

- literal `&`, `<`, `>` in text → write `&amp;`, `&lt;`, `&gt;`;
- HTML entities like `&nbsp;` → XML has no DTD; use numeric references (`&#160;`) or a space;
- an `old` string that cuts through a tag (ends inside `<w:r>`) while `new` does not restore it
  → extend `old` to whole `<w:p>…</w:p>` or `<w:r>…</w:r>` elements;
- a `new` string that opens `<w:p>`, `<w:r>`, `<w:t>` (or `<row>`, `<c>`) without closing it.

After a substantial edit, read the changed region back and check that every element you
opened is closed before you pack.

A `.docx` has several content parts (body, headers, footers, footnotes); an `.xlsx` has one
`xl/worksheets/sheetN.xml` per sheet plus `xl/sharedStrings.xml`. Edits are scoped to the part
you address, so a placeholder that recurs is edited in each part; a search over the unpacked
folder shows every part containing it.

## DOCX

### How replacements work

Use the **literal placeholder text** (`[[Datum]]`, `[[Name]]`) as the `old` string and target
the body part, `word/document.xml`. Word may split a placeholder across several `<w:r>`/`<w:t>`
runs (spell-check and revision tracking do this), and then the literal will not match. When a
replacement reports that the string was not found, search for a distinctive fragment (`[[Na`)
to see the run-split XML, then use that XML as the `old` string — usually replacing the whole
`<w:r>…</w:r>` sequence with a single run.

**Fill a template:** unpack `Briefkopf.docx` into `doc/`; search `doc/` for `[[`; in
`doc/word/document.xml` replace `[[Datum]]` with `06. März 2026` and `[[Name]]` with
`Max Mustermann`; in `doc/word/header1.xml` replace `[[Date]]` with `06.03.2026`; pack `doc/`
into `Angebot.docx`.

### Paragraph-level replacement

To insert paragraphs with specific formatting (bold, centred, a heading, a clause), make the
`old` string cover the whole `<w:p>…</w:p>` you are replacing and the `new` string the new
paragraph XML, for example:

```xml
<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>§ 20 Dienstreisen</w:t></w:r></w:p><w:p><w:r><w:t>(1) Flugreisen in der Business Class.</w:t></w:r></w:p>
```

Read how the template formats its existing paragraphs first and model your XML on those
patterns; a style referenced by `w:pStyle` must exist in `word/styles.xml`.

## XLSX

### Modify an existing sheet

Unpack `template.xlsx` into `xl/`. Text cells usually point into `xl/xl/sharedStrings.xml`
(`t="s"` with an index), so replace `[[Title]]` there; numbers sit in the sheet part as `<v>`
values, so replace `<v>0</v>` in `xl/xl/worksheets/sheet1.xml` — all occurrences only if every
zero really becomes the same number. Pack `xl/` into `report.xlsx`.

### Add a new sheet

A sheet is a new part and needs four coordinated changes inside the unpacked folder:

1. Read `xl/worksheets/sheet1.xml` to copy its shape, and write the new sheet as
   `xl/worksheets/sheet2.xml`.
2. In `xl/_rels/workbook.xml.rels`, add a `Relationship` for it with a new, unique `rId`.
3. In `xl/workbook.xml`, add a `<sheet>` element whose `r:id` is that `rId` and whose
   `sheetId` is unique.
4. In `[Content_Types].xml`, replace `</Types>` with
   `<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>`.

## PPTX

Slides are `ppt/slides/slideN.xml`, each with `ppt/slides/_rels/slideN.xml.rels`, listed in
`ppt/presentation.xml` and `ppt/_rels/presentation.xml.rels`. Replace text inside existing
`<a:t>` elements; adding a slide follows the same four-part recipe as a new sheet (part,
relationships, presentation list, `[Content_Types].xml`).
