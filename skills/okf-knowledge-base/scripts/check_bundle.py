#!/usr/bin/env python3
"""Check a knowledge bundle: conformance errors, likely mistakes, structure notes.

Usage:  check_bundle.py [BUNDLE_DIR]     (default: current directory)

Exit status is 1 when there is at least one ERROR, otherwise 0.
ERROR   breaks the format: the bundle is not conformant.
WARN    allowed by the format but almost always a mistake.
NOTE    a structure or naming habit worth fixing while you are in the file.

Uses PyYAML when it is importable for exact frontmatter checks, and falls back
to text checks when it is not. The fallback never reports a false ERROR.
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - depends on the environment
    yaml = None

RESERVED = {"index.md", "log.md"}
STATUSES = {"draft", "stable", "deprecated"}
MAX_DEPTH = 3          # directory levels below the bundle root
BIG_DIR = 25           # concepts in one directory before it wants splitting
INDEX_WANTED = 5       # concepts in one directory before it wants an index.md

TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})$")
ACTOR = re.compile(r"^(human:\S+|process:\S+|[\w.-]+/[\w.-]+)$")
AUTHOR = re.compile(r"^(human:\S+|process:\S+|team:\S+|[\w.-]+/[\w.-]+)$")
DATE_HEADING = re.compile(r"^##\s+(\S+)")
LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)>\s]+)>?\s*(?:\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
FILENAME = re.compile(r"^[a-z0-9][a-z0-9._-]*\.md$")


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, path, message):
        self.rows.append((level, path, message))

    def count(self, level):
        return sum(1 for r in self.rows if r[0] == level)

    def print(self):
        order = {"ERROR": 0, "WARN": 1, "NOTE": 2}
        for level, path, message in sorted(self.rows, key=lambda r: (order[r[0]], r[1])):
            print(f"{level:5}  {path}: {message}")


def split_frontmatter(text):
    """Return (frontmatter_text, body_text, had_block)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", text, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:]), True
    return "", text, False


def strip_code(text):
    out, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def links_in(text):
    targets = []
    for target in LINK.findall(strip_code(text)):
        if re.match(r"^(https?:|mailto:|#|\{)", target):
            continue
        targets.append(target.split("#", 1)[0])
    return [t for t in targets if t]


def as_datetime(value):
    """An aware datetime when the value is a valid OKF timestamp, else None.

    PyYAML turns an unquoted ISO timestamp into a datetime and a bare date into
    a date, so both shapes reach here alongside plain strings.
    """
    if isinstance(value, datetime):
        return value if value.tzinfo else None
    if not isinstance(value, str) or not TIMESTAMP.match(value.strip()):
        return None
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def walk_frontmatter_values(node, key_path=()):
    """Yield (key, value) for every scalar in a parsed frontmatter tree."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_frontmatter_values(value, key_path + (str(key),))
    elif isinstance(node, list):
        for item in node:
            yield from walk_frontmatter_values(item, key_path)
    else:
        yield key_path, node


def check_concept(rel, text, report):
    front, body, had_block = split_frontmatter(text)
    if not had_block:
        report.add("ERROR", rel, "no YAML frontmatter block delimited by --- at the top of the file")
        return
    data = None
    if yaml is not None:
        try:
            data = yaml.safe_load(front)
        except Exception as exc:  # noqa: BLE001 - any parse failure is the finding
            report.add("ERROR", rel, f"frontmatter is not parseable YAML: {exc}")
            return
        if data is not None and not isinstance(data, dict):
            report.add("ERROR", rel, "frontmatter is not a mapping of keys to values")
            return
        data = data or {}
        if not str(data.get("type") or "").strip():
            report.add("ERROR", rel, "frontmatter has no non-empty `type`")
        for key in ("title", "description"):
            if not str(data.get(key) or "").strip():
                report.add("WARN", rel, f"no `{key}` (index entries and search snippets use it)")
        status = data.get("status")
        if status is not None and str(status) not in STATUSES:
            report.add("WARN", rel, f"`status: {status}` is not draft, stable or deprecated")
        if "verified" in data and "generated" not in data:
            report.add("WARN", rel, "`verified` without `generated`: record who wrote it as well as who checked it")
        if "timestamp" in data and "generated" not in data:
            report.add("WARN", rel, "`timestamp` is the retired v0.1 field; use `generated: { by, at }`")
        for key_path, value in walk_frontmatter_values(data):
            leaf = key_path[-1] if key_path else ""
            text_value = str(value)
            if leaf in ("at", "stale_after", "last_modified", "from", "to"):
                when = as_datetime(value)
                if when is None:
                    report.add("WARN", rel, f"`{'.'.join(key_path)}: {value}` is not an ISO 8601 time with a UTC offset")
                elif leaf == "stale_after" and when <= datetime.now(timezone.utc):
                    report.add("WARN", rel, f"`stale_after: {value}` has passed: re-check the content or move the date")
            if leaf == "by" and not ACTOR.match(text_value):
                report.add("WARN", rel, f"`{'.'.join(key_path)}: {value}` is not human:<id>, process:<id> or <producer>/<version>")
            if leaf == "author" and not AUTHOR.match(text_value):
                report.add("WARN", rel, f"`{'.'.join(key_path)}: {value}` is not human:<id>, team:<id>, process:<id> or <producer>/<version>")
        ids = {str(s.get("id")) for s in data.get("sources", []) if isinstance(s, dict) and s.get("id")}
        for label in re.findall(r"\[\^([^\]]+)\]:", body):
            if label not in ids:
                report.add("WARN", rel, f"footnote [^{label}] has no matching `sources` entry with that `id`")
        if str(data.get("type") or "") == "Attested Computation":
            if not data.get("runtime"):
                report.add("ERROR", rel, "an Attested Computation needs `runtime`")
            has_file = bool(data.get("computation"))
            has_fence = bool(re.search(r"^#\s+Computation\s*$", body, re.M))
            if not has_file and not has_fence:
                report.add("ERROR", rel, "an Attested Computation needs either `computation:` or a `# Computation` body section")
            if has_file and has_fence:
                report.add("WARN", rel, "both `computation:` and a `# Computation` body section: keep one")
    else:
        if not re.search(r"^type:\s*\S", front, re.M):
            report.add("ERROR", rel, "frontmatter has no non-empty `type`")
        for key in ("title", "description"):
            if not re.search(rf"^{key}:\s*\S", front, re.M):
                report.add("WARN", rel, f"no `{key}` (index entries and search snippets use it)")
        for key, value in re.findall(r"\b(at|stale_after|last_modified):\s*'?\"?([^,'\"}\n]+)", front):
            if not TIMESTAMP.match(value.strip()):
                report.add("WARN", rel, f"`{key}: {value.strip()}` is not an ISO 8601 time with a UTC offset")
        for value in re.findall(r"\bby:\s*'?\"?([^,'\"}\n]+)", front):
            if not ACTOR.match(value.strip()):
                report.add("WARN", rel, f"`by: {value.strip()}` is not human:<id>, process:<id> or <producer>/<version>")


def check_index(rel, text, at_root, report):
    front, _, had_block = split_frontmatter(text)
    if had_block:
        keys = re.findall(r"^([A-Za-z_][\w-]*):", front, re.M)
        if not at_root or [k for k in keys if k != "okf_version"]:
            report.add("ERROR", rel, "index.md carries frontmatter (only a bundle-root `okf_version` is allowed)")


def check_log(rel, text, report):
    _, body, _ = split_frontmatter(text)
    dates = []
    for line in body.splitlines():
        match = DATE_HEADING.match(line)
        if not match:
            continue
        value = match.group(1)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            report.add("ERROR", rel, f"date heading `## {value}` is not ISO 8601 YYYY-MM-DD")
        else:
            dates.append(value)
    if dates and dates != sorted(dates, reverse=True):
        report.add("WARN", rel, "entries are not newest first")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bundle", nargs="?", default=".", help="bundle root directory")
    args = parser.parse_args()
    root = os.path.abspath(args.bundle)
    if not os.path.isdir(root):
        print(f"not a directory: {args.bundle}", file=sys.stderr)
        return 2

    report = Report()
    concepts = set()          # bundle-relative paths of concept files
    directories = {}          # directory -> (concept files, subdirectories)
    absolute_links = relative_links = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        reldir = os.path.relpath(dirpath, root)
        reldir = "" if reldir == "." else reldir
        md = sorted(f for f in filenames if f.endswith(".md"))
        directories[reldir] = ([f for f in md if f not in RESERVED], list(dirnames))
        for name in md:
            rel = os.path.join(reldir, name) if reldir else name
            if name not in RESERVED:
                concepts.add(rel)
            if not FILENAME.match(name):
                report.add("NOTE", rel, "file name is not lowercase letters, digits, hyphens or underscores")

    for dirpath, _, filenames in os.walk(root):
        reldir = os.path.relpath(dirpath, root)
        reldir = "" if reldir == "." else reldir
        if any(part.startswith(".") for part in reldir.split(os.sep) if part):
            continue
        for name in sorted(f for f in filenames if f.endswith(".md")):
            rel = os.path.join(reldir, name) if reldir else name
            with open(os.path.join(dirpath, name), encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            if name == "index.md":
                check_index(rel, text, at_root=(reldir == ""), report=report)
            elif name == "log.md":
                check_log(rel, text, report)
            else:
                check_concept(rel, text, report)

            for target in links_in(text):
                if target.startswith("/"):
                    absolute_links += 1
                    resolved = os.path.normpath(os.path.join(root, target.lstrip("/")))
                else:
                    relative_links += 1
                    resolved = os.path.normpath(os.path.join(dirpath, target))
                if not os.path.exists(resolved):
                    report.add("WARN", rel, f"link target does not exist: {target}")

    for reldir, (files, subdirs) in sorted(directories.items()):
        shown = reldir or "."
        depth = len([p for p in reldir.split(os.sep) if p])
        has_index = os.path.exists(os.path.join(root, reldir, "index.md"))
        if depth > MAX_DEPTH:
            report.add("NOTE", shown, f"{depth} levels below the bundle root: flatten it or move the group up")
        if len(files) == 1 and not subdirs and depth > 0:
            report.add("NOTE", shown, "directory holds one concept: keep it in the parent until there are more")
        if len(files) > BIG_DIR and not subdirs:
            report.add("NOTE", shown, f"{len(files)} concepts in one directory: group the largest kind into a subdirectory")
        if len(files) >= INDEX_WANTED and not has_index:
            report.add("NOTE", shown, f"{len(files)} concepts and no index.md: add one so a reader can see the group without opening files")
        if not has_index:
            continue

        with open(os.path.join(root, reldir, "index.md"), encoding="utf-8", errors="replace") as handle:
            index_text = handle.read()
        listed = set()
        for target in links_in(index_text):
            base = os.path.join(root, reldir)
            resolved = os.path.normpath(os.path.join(root, target.lstrip("/")) if target.startswith("/")
                                        else os.path.join(base, target))
            listed.add(os.path.relpath(resolved, root))
            if os.path.basename(resolved) == "index.md":
                listed.add(os.path.relpath(os.path.dirname(resolved), root))
        index_rel = os.path.join(reldir, "index.md") if reldir else "index.md"
        for name in files:
            entry = os.path.join(reldir, name) if reldir else name
            if entry not in listed:
                report.add("WARN", index_rel, f"does not list {name}")
        for sub in subdirs:
            entry = os.path.join(reldir, sub) if reldir else sub
            if entry not in listed:
                report.add("WARN", index_rel, f"does not list the {sub}/ subdirectory")

    if absolute_links and relative_links:
        report.add("NOTE", ".", f"mixed link styles: {absolute_links} bundle-absolute and {relative_links} relative. Pick one for the whole bundle")

    report.print()
    errors, warns, notes = report.count("ERROR"), report.count("WARN"), report.count("NOTE")
    engine = "PyYAML" if yaml else "text checks only (PyYAML not importable)"
    print(f"\n{len(concepts)} concepts in {len(directories)} directories, {engine}."
          f" {errors} error(s), {warns} warning(s), {notes} note(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
