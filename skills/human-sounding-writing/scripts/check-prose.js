/**
 * Checks a draft for what makes text read as machine-written: sentences of one length, sentences
 * that run long, and dashes standing in for commas. Pass the draft as `text`; the last expression
 * is the report. Under Node, pass a file instead: `node scripts/check-prose.js draft.md`.
 *
 * A leading YAML frontmatter block, code blocks, inline code, link targets and Markdown markers
 * are left out before counting, so a list or a heading is not read as a run of short sentences,
 * and a dash quoted as code is not counted as one.
 */

const LONG_SENTENCE = 30;
const SAME_LENGTH = 2;
const SAME_LENGTH_RUN = 3;
const FLAT_SPREAD = 5;

/** Abbreviations whose full stop does not end a sentence. */
const ABBREVIATIONS = ["e.g.", "i.e.", "etc.", "vs.", "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "St.", "No.", "approx."];

/**
 * The draft without a leading YAML frontmatter block, each of its lines left empty so a dash is
 * reported on the line it has in the file.
 */
function body(text) {
  return text
    .replace(/\r\n?/g, "\n")
    .replace(/^---\n[\s\S]*?\n---(?:\n|$)/, (frontmatter) => "\n".repeat(frontmatter.split("\n").length - 1));
}

/** The draft as running prose: code, link targets and Markdown markers left out. */
function prose(text) {
  return text
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`[^`]*`/g, "code")
    .replace(/\]\([^)]*\)/g, "]")
    // A heading is no sentence, and a list item ends one even without a full stop.
    .replace(/^\s{0,3}#{1,6}\s+.*$/gm, "\n")
    .replace(/^\s*(?:[-*+]|\d+[.)])\s+/gm, "\n\n")
    .replace(/[*_]{1,3}([^*_]+)[*_]{1,3}/g, "$1");
}

/** The draft's sentences, each as its words. */
function sentencesOf(text) {
  let body = prose(text);
  ABBREVIATIONS.forEach((abbreviation, index) => {
    body = body.split(abbreviation).join(abbreviation.replace(/\./g, `\u0000${index}`));
  });
  return body
    .split(/(?<=[.!?])["')\]]*\s+|\n{2,}/)
    .map((sentence) => sentence.replace(/\u0000\d+/g, ".").trim())
    .filter((sentence) => /[A-Za-z0-9]/.test(sentence))
    .map((sentence) => ({ sentence, words: sentence.split(/\s+/).filter((word) => /[A-Za-z0-9]/.test(word)) }));
}

/** Every dash that stands in for a comma, with its line and what surrounds it; code is skipped. */
function dashesOf(text) {
  const found = [];
  let fenced = false;
  text.split("\n").forEach((line, index) => {
    if (/^\s*```/.test(line)) fenced = !fenced;
    if (fenced || /^\s*(```|---\s*$)/.test(line)) return;
    // Inline code keeps its width, so the context shown is still the line's.
    const scanned = line.replace(/`[^`]*`/g, (code) => " ".repeat(code.length));
    for (const match of scanned.matchAll(/—|\s–\s|\s--\s/g)) {
      const at = match.index ?? 0;
      found.push({
        line: index + 1,
        dash: match[0].trim() === "—" ? "em dash" : match[0].trim() === "–" ? "en dash" : "double hyphen",
        context: line.slice(Math.max(0, at - 30), at + 30).trim(),
      });
    }
  });
  return found;
}

function check(text) {
  const sentences = sentencesOf(String(text ?? ""));
  const lengths = sentences.map(({ words }) => words.length);
  const words = lengths.reduce((sum, length) => sum + length, 0);
  const meanLength = lengths.length ? words / lengths.length : 0;
  const spread = lengths.length
    ? Math.sqrt(lengths.reduce((sum, length) => sum + (length - meanLength) ** 2, 0) / lengths.length)
    : 0;

  const longSentences = sentences
    .filter(({ words }) => words.length > LONG_SENTENCE)
    .map(({ words }) => ({ words: words.length, start: words.slice(0, 8).join(" ") + " …" }));

  const sameLengthRuns = [];
  let start = 0;
  for (let index = 1; index <= lengths.length; index += 1) {
    const inRun = index < lengths.length && Math.abs(lengths[index] - lengths[start]) <= SAME_LENGTH;
    if (inRun) continue;
    if (index - start >= SAME_LENGTH_RUN) {
      sameLengthRuns.push({ sentences: index - start, around: lengths[start], start: sentences[start].words.slice(0, 8).join(" ") + " …" });
    }
    start = index;
  }

  const dashes = dashesOf(String(text ?? ""));
  const advice = [];
  if (dashes.length) advice.push(`Replace ${dashes.length} dash${dashes.length === 1 ? "" : "es"} with a comma, a colon, parentheses or a new sentence.`);
  if (longSentences.length) advice.push(`Break ${longSentences.length} sentence${longSentences.length === 1 ? "" : "s"} over ${LONG_SENTENCE} words.`);
  if (sameLengthRuns.length) advice.push(`Vary ${sameLengthRuns.length} run${sameLengthRuns.length === 1 ? "" : "s"} of ${SAME_LENGTH_RUN} or more sentences of about the same length.`);
  if (lengths.length >= 5 && spread < FLAT_SPREAD) advice.push(`Sentence lengths vary too little (spread ${spread.toFixed(1)} words): mix short sentences with longer ones.`);

  return {
    verdict: advice.length ? "revise" : "ok",
    advice,
    sentences: lengths.length,
    words,
    meanLength: Number(meanLength.toFixed(1)),
    spread: Number(spread.toFixed(1)),
    longSentences,
    sameLengthRuns,
    dashes,
  };
}

/* The script's input: `args.text` from an agent, or a file named on Node's command line. */
const input =
  typeof args !== "undefined" && args && typeof args.text === "string"
    ? args.text
    : typeof process !== "undefined" && process.argv && process.argv[2]
      ? (await import("node:fs")).readFileSync(process.argv[2], "utf8")
      : "";

const report = check(body(input));
if (typeof args === "undefined" && typeof console !== "undefined") console.log(JSON.stringify(report, null, 2));
report;
