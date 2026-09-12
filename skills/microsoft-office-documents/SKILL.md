---
name: Microsoft Office Documents
description: Fill in and edit Word, Excel and PowerPoint files — letters, spreadsheets and slide decks — starting from an existing template. Read this before creating or changing any DOCX, XLSX or PPTX file.
tools:
  - Unpack a file archive into a folder, and pack a folder back into one file
  - List, read, search and edit files as text
  - Copy or move a file without opening it (to copy a template, and for pictures)
  - View a document's text and tables
  - Send or store the finished file
---

# Microsoft Office documents

An Office document is a zip container of XML parts. You never write the binary; you unpack
the container, edit the parts as text, and pack it again.

## What you need

This skill assumes the capabilities listed in its frontmatter. Check that you have each
before you start; if one is missing, say which and stop rather than improvising.

- **Unpack a container** — a tool that takes a file you hold and extracts every entry into a
  directory, preserving the entry paths inside the container (`word/document.xml`,
  `[Content_Types].xml`). Office files are zips, so any tool that unpacks a `.zip` unpacks a
  `.docx`.
- **Pack a directory** — a tool that zips a directory back into one file, keeping paths
  relative to the directory and the file extension you give the result. This is what turns
  the edited directory into a valid `.docx`, `.xlsx` or `.pptx`.
- **Read and edit files as text** — list a directory, read a file, search files for a string,
  and replace one exact string with another in a file. Writing a whole new file is needed only
  when adding a part, such as a new sheet.
- **Move or copy a file** — to copy a template to the name your document should have before
  you unpack it, and for images: placing a picture you hold into the unpacked directory as a
  media part, or swapping one media part for another. A text editor cannot do the latter;
  image bytes are never read or written as text.
- **Render a document as text** — a tool that shows a document's prose and tables as markdown.
  Use it to read; it never edits.
- **Deliver the finished file** — a tool that sends, stores or forwards a file you hold, or
  turns it into a download link. Without one the document never leaves your working directory.

Files are referred to by the paths your file tools report, relative to your working
directory. Never paste a file's bytes into a tool argument.

## Core rules

1. **Never write a `.docx`, `.xlsx` or `.pptx` from scratch.** Derive it from a template: a
   document attached to this conversation, one in a directory you were given, one you
   fetched from a link, or — when nobody supplies one — a copy of the blank template that
   ships beside this file (see "Blank templates"). List and search your working directory
   before asking. Raw OOXML written by hand yields missing styles and files Office refuses to
   open. A supplied template beats a blank one whenever the document needs a house style,
   letterhead or logo, so if the request implies one and none is there, ask — and if nobody
   is watching this session, ask through the channel the request came from.
2. **Read as text, edit as parts.** Render the whole document to see what it says. Change it by
   unpacking, editing parts, packing.
3. **Nothing checks your XML.** A part that is no longer well-formed produces a document Office
   rejects, and no tool warns you. Keep every edit inside whole elements and escape text (see
   "XML must stay well-formed").
4. **Deliver with a tool.** A packed document in your working directory reaches nobody by
   itself:
   attach it with the tool that sends messages, hand it to the tool that stores or forwards
   files, or create a download link when a person or system needs one.

## Blank templates

Three empty but valid documents sit next to this file, for when the request supplies no
template of its own:

| File | What is in it |
| --- | --- |
| `template.docx` | one empty paragraph, A4 portrait, default Word styles |
| `template.xlsx` | one empty sheet named `Tabelle1` |
| `template.pptx` | one title slide (title and subtitle placeholders), 16:9, Office theme |

They hold no content and no author metadata, so they are a clean start rather than someone
else's document with the text taken out.

**Copy one, never work on it in place.** Copy the file into your working directory under the
name the finished document should have, then unpack that copy and edit it. Unpacking or
packing over the template itself leaves the next document starting from your leftovers.

A blank template carries no letterhead, logo or corporate styling. When the request wants
those, it needs a real template — the blank one cannot stand in for it.

### Language

The blank templates are set to German (`de-DE`). That setting does not translate anything; it
decides the proofing language and the locale Word and PowerPoint assume, so leave it alone
for a German document and change it for any other. Each format keeps it elsewhere:

- **DOCX** — `w:val` on `<w:lang>` in `word/styles.xml` (the `docDefaults` run properties),
  and `<w:themeFontLang w:val="de-DE"/>` in `word/settings.xml`. Runs that carry their own
  `<w:lang>` override the default, so search the unpacked directory for `w:lang` rather than
  trusting the two above.
- **PPTX** — a `lang="de-DE"` attribute on every `<a:rPr>`, `<a:endParaRPr>` and `<a:defRPr>`,
  spread over `ppt/slides/`, `ppt/slideLayouts/` and `ppt/slideMasters/`. This is one of the
  rare edits where replacing all occurrences of `lang="de-DE"` in each part really is the same
  edit everywhere.
- **XLSX** — cells have no language. What is German is the sheet name `Tabelle1`; rename it in
  `<sheet name="Tabelle1" .../>` in `xl/workbook.xml`, and change the matching `<vt:lpstr>` in
  `docProps/app.xml` so the two agree.

The same applies to a supplied template: it is written in some language already, and the
document you produce should keep it unless the request says otherwise.

## Workflow: unpack → edit → pack

1. Unpack the template into a directory of its own inside your working directory, one per
   document, so two documents never mix parts.
2. List that directory to see the parts; search it for your placeholders (for example `[[`) to
   learn which part holds each one — a date may sit in the body and in a header.
3. Read the part you will change to see its actual XML around the placeholder.
4. Replace strings, one region per edit.
5. Pack the directory into a file whose name carries the right extension, then deliver it.

Notes:

- Do not add or remove files in the unpacked directory unless you also update
  `[Content_Types].xml` and the relationship parts (see "Add a new sheet").
- Address `[Content_Types].xml` by its exact path with read and edit. Do not use a glob pattern
  for it: the brackets are a character class in glob syntax.
- Word and Excel emit their XML as one very long line. Search first to locate the region, then
  replace with an `old` string that is unique and short. Replace one region per edit rather than
  rewriting a whole `document.xml` or `sheetN.xml`; a rewritten part is a part you had to
  reproduce perfectly.

## Reading a document

1. Render the container as markdown to confirm it is the right file and see its shape.
2. Unpack it and list the unpacked directory to see the parts.
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
directory shows every part containing it.

## DOCX

### How replacements work

Use the **literal placeholder text** (`[[Datum]]`, `[[Name]]`) as the `old` string and target
the body part, `word/document.xml`. Word may split a placeholder across several `<w:r>`/`<w:t>`
runs (spell-check and revision tracking do this), and then the literal will not match. When a
replacement reports that the string was not found, search for a distinctive fragment (`[[Na`)
to see the run-split XML, then use that XML as the `old` string — usually replacing the whole
`<w:r>…</w:r>` sequence with a single run.

**Fill a template:** unpack the letterhead template into its own directory; search that
directory for `[[`; in its `word/document.xml` replace `[[Datum]]` with `06. März 2026` and
`[[Name]]` with `Max Mustermann`; in its `word/header1.xml` replace `[[Date]]` with
`06.03.2026`; pack the directory into a `.docx` with the name the request asks for.

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

Unpack the workbook template into its own directory. Text cells usually point into
`xl/sharedStrings.xml` (`t="s"` with an index), so replace `[[Title]]` there; numbers sit in
the sheet part as `<v>` values, so replace `<v>0</v>` in `xl/worksheets/sheet1.xml` — all
occurrences only if every zero really becomes the same number. Pack the directory into an
`.xlsx`.

### Add a new sheet

A sheet is a new part and needs four coordinated changes inside the unpacked directory:

1. Read `xl/worksheets/sheet1.xml` to copy its shape, and write the new sheet as
   `xl/worksheets/sheet2.xml`.
2. In `xl/_rels/workbook.xml.rels`, add a `Relationship` for it with a new, unique `rId`.
3. In `xl/workbook.xml`, add a `<sheet>` element whose `r:id` is that `rId` and whose
   `sheetId` is unique.
4. In `[Content_Types].xml`, replace `</Types>` with
   `<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>`.

## Images

Pictures are **media parts**: binary files under `word/media/` (Word), `xl/media/` (Excel)
or `ppt/media/` (PowerPoint), reached from a content part through a relationship. Three
things tie one together:

- the media file itself, for example `word/media/image1.png`;
- a `Relationship` in the content part's `.rels` file (`word/_rels/document.xml.rels`,
  `ppt/slides/_rels/slide1.xml.rels`) with `Type=".../relationships/image"`, a `Target`
  pointing at the media file, and an `Id` such as `rId5`;
- a reference to that `Id` inside the content XML: `<a:blip r:embed="rId5"/>` in a
  `<w:drawing>` (Word) or `<p:pic>` (PowerPoint).

The file's extension must also be declared once in `[Content_Types].xml` as a `Default`
(`<Default Extension="png" ContentType="image/png"/>`); templates that already contain a
picture of that type have it, templates that do not need it added.

Never open a media file with a text tool: reading it shows noise and writing it corrupts it.
Move or copy the file as bytes.

### Replace a picture, keep its place and size

The simplest and most reliable operation. Find which media file the picture is: search the
content part for `r:embed`, take the `rId`, look it up in the `.rels` file to get the
`Target`. Then copy your new image over that media file **under the same name**. Nothing
else changes: the relationship, the placement and the declared size stay as the template
had them. A logo swap, a signature, a product photo in a fixed frame all work this way.

The picture is drawn at the size the XML declares, not the image's own size, so a
replacement with a different aspect ratio is stretched. Match the original's proportions, or
adjust the extent (see below).

### Insert a new picture

Adding a picture is a new part with the same four-part discipline as a new sheet:

1. Copy the image into the media directory under a new, unused name (`image7.png`).
2. In the content part's `.rels`, add
   `<Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image7.png"/>`
   with an `Id` unused in that file.
3. Ensure `[Content_Types].xml` has a `Default` for the extension.
4. In the content XML, insert a drawing that references the `Id`. Do not write one from
   memory: copy an existing `<w:drawing>…</w:drawing>` (or `<p:pic>…</p:pic>`) from the
   template, change its `r:embed` to the new `Id`, give its `wp:docPr` a new unique `id`,
   and set its size.

If the template contains no picture at all, prefer asking for a template that does, or
replacing a picture in a template that has one, over composing drawing XML by hand.

### Size and position

Sizes are in EMUs: 914400 per inch, 360000 per centimetre. A picture 6 cm wide is
`cx="2160000"`. Set the same values in both places Word keeps them — `<wp:extent cx cy/>`
and `<a:ext cx cy/>` inside the drawing — and keep the aspect ratio of the image. Inline
pictures (`<wp:inline>`) flow with the text and are the easy case; anchored pictures
(`<wp:anchor>`) carry positioning that is best left as the template had it.

### Excel and PowerPoint

In Excel a picture belongs to a drawing part (`xl/drawings/drawing1.xml`) that the sheet
references through its own `.rels`; the media relationship lives in
`xl/drawings/_rels/drawing1.xml.rels`. Replacing the media file by name works exactly as in
Word. In PowerPoint each slide's `.rels` holds its own image relationships, so the same
`rId` may mean different pictures on different slides — always read the `.rels` of the slide
you are editing.

## PPTX

Slides are `ppt/slides/slideN.xml`, each with `ppt/slides/_rels/slideN.xml.rels`, listed in
`ppt/presentation.xml` and `ppt/_rels/presentation.xml.rels`. Replace text inside existing
`<a:t>` elements; adding a slide follows the same four-part recipe as a new sheet (part,
relationships, presentation list, `[Content_Types].xml`).
