---
name: OOXML documents
description: Fill and edit Word (.docx), Excel (.xlsx) and PowerPoint (.pptx) documents from a template by unpacking, editing the XML parts and packing again. Read this before creating or changing any Office document.
---

# OOXML documents

How to produce Word, Excel and PowerPoint files with the platform's file tools. An Office
document is a zip container of XML parts; you edit the parts, never the binary.

## Tools you need

- `files__unpack_file` — unpacks a container held as a turn file into a turn folder.
- `files__pack_files` — packs a turn folder back into one container.
- `get_markdown` — renders a document as text, for reading only.
- `read_file`, `edit_file`, `write_file`, `ls`, `glob`, `grep` — work on the unpacked parts.

The two `files__…` actions belong to the credential-free `files` collection; the workflow state
that produces documents has to grant them in `tools.allow`. If a call is refused, say so and
stop — you cannot produce the document without them.

Files are addressed by **turn-file reference**: a path relative to your turn folder, such as
`attachments/template.docx` or `scratchpad/doc/word/document.xml`. Never put a file's bytes
into a tool argument.

## Core rules

1. **Never write a `.docx`, `.xlsx` or `.pptx` from scratch.** Always derive it from a
   template: a document uploaded to this turn (under `attachments/`), one in a data folder
   this state mounts, or one fetched with `files__download_file`. Find candidates with `ls`
   or `glob` before asking. Raw OOXML written by hand yields missing styles and files Office
   refuses to open. If no template exists, ask for one; in a session nobody is watching,
   ask through the channel the request came from.
2. **Read as text, edit as parts.** `get_markdown` on the whole file tells you what it says.
   Editing goes through `files__unpack_file`, `edit_file` and `files__pack_files`.
3. **Nothing checks your XML.** A part that is no longer well-formed produces a document
   Office rejects, and no tool will warn you. Keep every edit inside whole elements and
   escape text (see "XML must stay well-formed").
4. **Deliver with a tool.** A packed document under `scratchpad/` reaches nobody by itself:
   attach it with the mail tool, hand it to whatever tool sends files onward, or create a link
   with `files__create_presigned_url` when a person or system needs to download it.

## Workflow: unpack → edit → pack

```
files__unpack_file(reference: "attachments/template.docx", destination: "scratchpad/doc")
ls("scratchpad/doc")                                            — the container's parts
grep(pattern: "[[", path: "scratchpad/doc")                     — every placeholder, with its part
read_file(file_path: "scratchpad/doc/word/document.xml")        — the body, as raw XML
edit_file(file_path: "scratchpad/doc/word/document.xml", old_string: "[[Name]]", new_string: "Max Mustermann")
edit_file(file_path: "scratchpad/doc/word/header1.xml",  old_string: "[[Date]]", new_string: "06.03.2026")
files__pack_files(source: "scratchpad/doc", destination: "scratchpad/Angebot.docx")
```

Notes:

- Unpack into its own folder per document (`scratchpad/doc`, `scratchpad/xl`), so a second
  document never mixes parts with the first. When `destination` is omitted a collision-free
  folder under `attachments/` is chosen for you; the result names it.
- `files__pack_files` keeps entry names relative to `source` and the destination's extension
  as given, so a folder that came from `files__unpack_file` packs into a valid `.docx`,
  `.xlsx` or `.pptx` when you name it one. Do not add or remove files in the folder unless you
  also update `[Content_Types].xml` and the relationships (see "Add a new sheet").
- Address `[Content_Types].xml` directly with `read_file` and `edit_file`. Do not `glob` for
  it: the brackets are a character class in glob patterns.
- Word and Excel emit their XML as one very long line. Prefer `grep` to locate the region you
  need, then `edit_file` with an `old_string` that is unique and short. Replace one region per
  call rather than rewriting a whole `document.xml` or `sheetN.xml`; a rewritten part is a
  part you had to reproduce perfectly.

## Reading a document

1. `get_markdown(path: "attachments/report.xlsx")` — the text, tables and list structure, to
   confirm it is the right file and see its shape.
2. `files__unpack_file(...)` then `ls` — the parts.
3. `read_file` on the part you will change — the raw XML.

`get_markdown` never changes anything and works on the container only; on an unpacked XML
part use `read_file`.

## Editing with `edit_file`

`edit_file(file_path, old_string, new_string, replace_all?)` replaces one occurrence, or all
with `replace_all: true`. It works on raw part content.

### XML must stay well-formed

The usual ways an edit breaks a part:

- literal `&`, `<`, `>` in text → write `&amp;`, `&lt;`, `&gt;`;
- HTML entities like `&nbsp;` → XML has no DTD; use numeric references (`&#160;`) or a space;
- an `old_string` that cuts through a tag (ends inside `<w:r>`) while `new_string` does not
  restore it → extend `old_string` to whole `<w:p>…</w:p>` or `<w:r>…</w:r>` elements;
- a `new_string` that opens `<w:p>`, `<w:r>`, `<w:t>` (or `<row>`, `<c>`) without closing it.

After a substantial edit, `read_file` the changed region and check that every element you
opened is closed before you pack.

A `.docx` has several content parts (body, headers, footers, footnotes); an `.xlsx` has one
`xl/worksheets/sheetN.xml` per sheet plus `xl/sharedStrings.xml`. Edits are scoped to the part
you address, so a placeholder that recurs (a date in the header and the body) is edited in
each part — `grep` over the unpacked folder shows every part containing it.

## DOCX

### How replacements work

Use the **literal placeholder text** as `old_string` (`[[Datum]]`, `[[Name]]`) and target the
body part, `word/document.xml`. Word may split a placeholder across several `<w:r>`/`<w:t>`
runs (spell-check and revision tracking do this), and then the literal will not match. When
`edit_file` reports that `old_string` was not found, `grep` for a distinctive fragment
(`[[Na`) to see the run-split XML, then use that XML as `old_string` — usually replacing the
whole `<w:r>…</w:r>` sequence with a single run.

**Fill a template:**

```
files__unpack_file(reference: "attachments/Briefkopf.docx", destination: "scratchpad/doc")
grep(pattern: "[[", path: "scratchpad/doc")
edit_file(file_path: "scratchpad/doc/word/document.xml", old_string: "[[Datum]]", new_string: "06. März 2026")
edit_file(file_path: "scratchpad/doc/word/document.xml", old_string: "[[Name]]",  new_string: "Max Mustermann")
edit_file(file_path: "scratchpad/doc/word/header1.xml",  old_string: "[[Date]]",  new_string: "06.03.2026")
files__pack_files(source: "scratchpad/doc", destination: "scratchpad/Angebot.docx")
```

### Paragraph-level replacement

To insert paragraphs with specific formatting (bold, centred, a heading, a clause), make
`old_string` cover the whole `<w:p>…</w:p>` you are replacing and `new_string` the new
paragraph XML:

```
edit_file(file_path: "scratchpad/doc/word/document.xml",
  old_string: "<w:p>…the original paragraph XML…</w:p>",
  new_string: "<w:p><w:pPr><w:jc w:val=\"center\"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>§ 20 Dienstreisen</w:t></w:r></w:p><w:p><w:r><w:t>(1) Flugreisen in der Business Class.</w:t></w:r></w:p>")
```

Read how the template formats its existing paragraphs first and model your XML on those
patterns; styles referenced by `w:pStyle` must exist in `word/styles.xml`.

## XLSX

### Modify an existing sheet

```
files__unpack_file(reference: "attachments/template.xlsx", destination: "scratchpad/xl")
edit_file(file_path: "scratchpad/xl/xl/sharedStrings.xml", old_string: "[[Title]]", new_string: "Q4 Report")
edit_file(file_path: "scratchpad/xl/xl/worksheets/sheet1.xml", old_string: "<v>0</v>", new_string: "<v>1234.56</v>", replace_all: true)
files__pack_files(source: "scratchpad/xl", destination: "scratchpad/report.xlsx")
```

Text cells usually point into `xl/sharedStrings.xml` (`t="s"` with an index); numbers sit in
the sheet as `<v>`. Use `replace_all: true` only when every occurrence really is the same edit.

### Add a new sheet

A sheet is a new part and needs four coordinated changes. In `scratchpad/xl/` after unpacking:

```
read_file(file_path: "scratchpad/xl/xl/worksheets/sheet1.xml")                       — copy the shape
write_file(file_path: "scratchpad/xl/xl/worksheets/sheet2.xml", content: "…")        — the new sheet
edit_file(file_path: "scratchpad/xl/xl/_rels/workbook.xml.rels", …)                  — add the Relationship
edit_file(file_path: "scratchpad/xl/xl/workbook.xml", …)                             — add the <sheet> element
edit_file(file_path: "scratchpad/xl/[Content_Types].xml",
  old_string: "</Types>",
  new_string: "<Override PartName=\"/xl/worksheets/sheet2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/></Types>")
```

The relationship id (`rId…`) in `workbook.xml.rels` must be unique and must match the
`r:id` on the new `<sheet>`; the `sheetId` must be unique too.

## PPTX

Slides are `ppt/slides/slideN.xml`, each with `ppt/slides/_rels/slideN.xml.rels`, listed in
`ppt/presentation.xml` and `ppt/_rels/presentation.xml.rels`. Replace text inside existing
`<a:t>` elements; adding a slide follows the same four-part recipe as a new sheet
(part, relationships, presentation list, `[Content_Types].xml`).
