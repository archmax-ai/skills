/**
 * Draws every skill's preview, `skills/<slug>/preview.svg`, from its `SKILL.md` frontmatter: the
 * skill's `icon` on a tile in its `color` at the centre, ringed by the capabilities its `tools`
 * list names, each a small badge joined to the tile, on the archmax gradient. Run it after
 * changing a skill:
 *
 *   npm install && npm run previews
 *
 * A preview is drawn, never edited by hand, so every skill's looks the same. Its corners are
 * square: whatever shows it, a card or a page, rounds them as it rounds itself. It is for
 * browsing only; a host leaves it out when it installs the skill.
 */
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { parse } from "yaml";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");
const ICONS = join(dirname(createRequire(import.meta.url).resolve("lucide-static/package.json")), "icons");

/** The appearance palette a skill's `color` names. */
const PALETTE = {
  sage: "#8c987f",
  rose: "#bca195",
  blue: "#c2d0e4",
  purple: "#8878a8",
  rust: "#bc8081",
  amber: "#bdac8a",
  teal: "#85aeab",
};
const BRAND = "#8878a8";
const INK = "#24212c";
const WIDTH = 400;
const HEIGHT = 225;

/**
 * The capability a `tools` entry names, as an icon: the first rule whose words the entry holds.
 * The entries are plain language, so this reads them the way a person would.
 */
const CAPABILITIES = [
  [/archive|unpack|\bzip\b/, "FileArchive"],
  [/date and time/, "CalendarClock"],
  [/schedule/, "Clock"],
  [/arrive at an email|messages that arrive|mailbox/, "Inbox"],
  [/send a message|email to a person|send or store/, "Send"],
  [/search the web|web page/, "Globe"],
  [/pdf|word files|spreadsheets|document'?s text|text of documents/, "FileSearch"],
  [/move or rename|copy or move/, "FolderInput"],
  [/as text/, "FilePen"],
];

const kebab = (name) => name.replace(/([a-z0-9])([A-Z])/g, "$1-$2").replace(/([A-Za-z])([0-9])/g, "$1-$2").toLowerCase();

function iconBody(name) {
  const svg = readFileSync(join(ICONS, `${kebab(name)}.svg`), "utf8");
  return svg.replace(/^[\s\S]*?<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "").trim();
}

function frontmatter(text) {
  const match = /^---\n([\s\S]*?)\n---/.exec(text);
  return match ? parse(match[1]) : {};
}

/** The distinct capabilities a skill's tools name, in the order it lists them, at most eight. */
function capabilities(tools) {
  const icons = [];
  for (const entry of tools ?? []) {
    const line = String(entry).toLowerCase();
    const rule = CAPABILITIES.find(([pattern]) => pattern.test(line));
    const icon = rule ? rule[1] : "Wrench";
    if (!icons.includes(icon)) icons.push(icon);
  }
  return icons.slice(0, 8);
}

function render(skill) {
  const centre = { x: WIDTH / 2, y: HEIGHT / 2 };
  const fill = PALETTE[skill.color] ?? BRAND;
  const around = capabilities(skill.tools);
  // On an ellipse around the tile, the first at the top, the rest evenly round it.
  const badges = around.map((icon, index) => {
    const angle = -Math.PI / 2 + (index * 2 * Math.PI) / around.length;
    return { icon, x: centre.x + Math.cos(angle) * 128, y: centre.y + Math.sin(angle) * 72 };
  });
  const lines = badges
    .map(({ x, y }) => `<line x1="${centre.x}" y1="${centre.y}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" />`)
    .join("\n    ");
  const dots = badges
    .map(
      ({ icon, x, y }) => `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)})">
      <circle r="19" fill="#ffffff" filter="url(#lift)" />
      <g transform="translate(-10 -10) scale(0.8333)" fill="none" stroke="${BRAND}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${iconBody(icon)}</g>
    </g>`,
    )
    .join("\n    ");
  const escape = (text) => String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" width="${WIDTH}" height="${HEIGHT}" role="img" aria-label="${escape(skill.name ?? "Skill")}">
  <defs>
    <linearGradient id="backdrop" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#c2d0e4" />
      <stop offset="0.45" stop-color="#c8c1d9" />
      <stop offset="0.78" stop-color="#ccb4c5" />
      <stop offset="1" stop-color="#c9a9ac" />
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.6">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.5" />
      <stop offset="1" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>
    <filter id="lift" x="-40%" y="-40%" width="180%" height="190%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#2a2238" flood-opacity="0.16" />
    </filter>
  </defs>
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#backdrop)" />
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#glow)" />
  <g stroke="${BRAND}" stroke-opacity="0.4" stroke-width="1.5" stroke-dasharray="3 4" stroke-linecap="round">
    ${lines}
  </g>
  <g>
    ${dots}
  </g>
  <rect x="${centre.x - 36}" y="${centre.y - 36}" width="72" height="72" rx="22" fill="${fill}" filter="url(#lift)" />
  <g transform="translate(${centre.x - 18} ${centre.y - 18}) scale(1.5)" fill="none" stroke="${INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${iconBody(skill.icon ?? "Sparkles")}</g>
</svg>
`;
}

for (const slug of readdirSync(SKILLS).sort()) {
  const skill = frontmatter(readFileSync(join(SKILLS, slug, "SKILL.md"), "utf8"));
  writeFileSync(join(SKILLS, slug, "preview.svg"), render(skill));
  console.log(`skills/${slug}/preview.svg`);
}
