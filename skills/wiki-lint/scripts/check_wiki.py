#!/usr/bin/env python3
"""Read-only checks for a Markdown wiki. Results are candidates for human review."""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit


WIKILINK = re.compile(r"\[\[([^\]\n]+)\]\]")
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\n)]+))\)")


def visible_text(text):
    """Mask fenced code and comments; retain inline text for raw-path checks."""
    def mask(match):
        return re.sub(r"[^\n]", " ", match.group())

    text = re.sub(r"<!--.*?-->", mask, text, flags=re.S)
    lines = text.splitlines(keepends=True)
    fence = None
    for i, line in enumerate(lines):
        opening = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if re.match(r"^\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            lines[i] = re.sub(r"[^\n]", " ", line)
        elif opening:
            fence = opening[1]
            lines[i] = re.sub(r"[^\n]", " ", line)
        else:
            # Inline code may contain raw paths that are useful evidence references;
            # leave its text available to the raw-reference scan below.
            lines[i] = line
    return "".join(lines)


def check(root, wiki_dir="wiki", raw_dir="raw", index="wiki/index.md", hubs=()):
    root = Path(root).resolve()
    wiki = (root / wiki_dir).resolve()
    raw = (root / raw_dir).resolve()
    index_path = (root / index).resolve()
    if not wiki.is_dir() or not raw.is_dir() or not index_path.is_file():
        raise ValueError("wiki directory, raw directory, and index must exist; check schema and path flags")
    if not index_path.is_relative_to(wiki):
        raise ValueError("index must be inside the configured wiki directory")

    pages = sorted(p.resolve() for p in wiki.rglob("*.md") if p.is_file())
    # Do not follow links to files outside the configured tree.
    pages = [p for p in pages if p.is_relative_to(wiki)]
    page_set = set(pages)
    by_name = defaultdict(list)
    for page in pages:
        by_name[page.stem].append(page)
    hub_paths = {index_path, wiki / "log.md", wiki / "overview.md"}
    hub_paths.update((root / h).resolve() for h in hubs)
    incoming = set()
    indexed = set()
    referenced_raw = set()
    findings = []

    def display(path):
        return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)

    def report(kind, page, line, message):
        findings.append(dict(kind=kind, file=display(page), line=line, message=message))

    def resolve_link(target, page):
        target = unquote(target.split("|", 1)[0].split("#", 1)[0]).strip()
        if not target:
            return [page]  # Heading-only links stay on the same page.
        if target.endswith(".md"):
            target = target[:-3]
        if "/" not in target:
            return by_name.get(target, [])
        if target.startswith(("./", "../")):
            candidate = page.parent / (target + ".md")
        else:
            candidate = wiki / (target + ".md")
            # Also accept vault-root-qualified links such as [[wiki/sources/x]].
            root_candidate = (root / (target + ".md")).resolve()
            if root_candidate in page_set:
                candidate = root_candidate
        candidate = candidate.resolve()
        return [candidate] if candidate in page_set else []

    raw_prefix = raw.relative_to(root).as_posix() if raw.is_relative_to(root) else raw.as_posix()
    bare_raw = re.compile(re.escape(raw_prefix) + r"/[^\s<>\[\]()\"'`,;:!?]+")

    def raw_reference(page, line, path):
        referenced_raw.add(path)
        if not path.is_file():
            report("broken-raw-reference", page, line, "Missing raw file: " + display(path))

    for page in pages:
        text = page.read_text(encoding="utf-8")
        visible = visible_text(text)
        if page not in hub_paths and len(text.splitlines()) < 10:
            report("stub", page, 1, "Fewer than 10 lines; verify whether the page is complete")
        for number, line in enumerate(visible.splitlines(), 1):
            # Inline code is not a wikilink. Raw paths in inline code are still checked.
            # Keep offsets stable so Markdown spans can also mask the original
            # line without discarding inline-code raw references.
            link_line = re.sub(r"(`+).*?\1", lambda m: " " * len(m[0]), line)
            for match in WIKILINK.finditer(link_line):
                targets = resolve_link(match[1], page)
                if not targets:
                    report("broken-wikilink", page, number, match[0])
                elif len(targets) > 1:
                    report("ambiguous-wikilink", page, number,
                           match[0] + ": " + ", ".join(display(p) for p in targets))
                else:
                    target = targets[0]
                    if page == index_path:
                        indexed.add(target)
                    elif target != page:
                        incoming.add(target)

            # Markdown paths resolve relative to the page, not the project root.
            spans = []
            for match in MARKDOWN_LINK.finditer(link_line):
                # Link labels, titles, and remote URLs are not bare raw paths.
                spans.append(match.span())
                destination = (match[1] or match[2]).strip()
                if match[1] is None:
                    destination = re.sub(r"\s+[\"'].*[\"']$", "", destination)
                parsed = urlsplit(destination)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                path = (page.parent / unquote(parsed.path)).resolve()
                if path.is_relative_to(raw):
                    raw_reference(page, number, path)
            # Remove link syntax before scanning bare root-relative raw paths.
            remainder = line
            for start, end in reversed(spans):
                remainder = remainder[:start] + " " * (end - start) + remainder[end:]
            # Preserve inline-code raw references, including filenames with spaces.
            quoted = re.compile(r"`([^`]+)`|\"([^\"]+)\"|'([^']+)'")
            for match in quoted.finditer(remainder):
                value = next(part for part in match.groups() if part is not None)
                if value.startswith(raw_prefix + "/"):
                    raw_reference(page, number, (root / unquote(value)).resolve())
                    remainder = remainder.replace(match[0], "")
            # The source field is a whole path, so unquoted YAML may contain spaces.
            source_field = re.match(r"^source:\s*(" + re.escape(raw_prefix) + r"/.+?)\s*$", remainder)
            if source_field:
                raw_reference(page, number, (root / unquote(source_field[1])).resolve())
            else:
                for match in bare_raw.finditer(remainder):
                    raw_reference(page, number, (root / unquote(match[0].rstrip("."))).resolve())

    for page in pages:
        if page not in hub_paths:
            if page not in indexed:
                report("index-missing-page", page, 1, "Page is absent from the index")
            if page not in incoming:
                report("orphan", page, 1, "No inbound link outside the index or the page itself")
    for path in sorted(raw.rglob("*")):
        if path.is_file() and path.resolve() not in referenced_raw:
            report("unreferenced-raw", path, 1, "No recognized reference from a wiki page")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="wiki project root")
    parser.add_argument("--wiki-dir", default="wiki", help="path relative to root, or absolute")
    parser.add_argument("--raw-dir", default="raw", help="path relative to root, or absolute")
    parser.add_argument("--index", default="wiki/index.md", help="path relative to root, or absolute")
    parser.add_argument("--hub", action="append", default=[], help="additional hub path relative to root; repeatable")
    args = parser.parse_args()
    try:
        findings = check(args.root, args.wiki_dir, args.raw_dir, args.index, args.hub)
    except (OSError, ValueError) as error:
        parser.exit(2, "Cannot check wiki: " + str(error) + "\n")
    print(json.dumps(findings, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
