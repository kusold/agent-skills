#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["tiktoken==0.12.0"]
# ///
"""Count skill source tokens locally; run with `uv run scripts/count_skill_tokens.py`."""

import argparse
import html
import json
from pathlib import Path

import tiktoken


DEFAULT_SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"


def markdown_report(skills, encoding_name):
    """Render a GitHub Actions summary with per-skill counts and totals."""
    def cell(value):
        return (html.escape(value).replace("\\", "&#92;").replace("|", "&#124;")
                .replace("`", "&#96;").replace("\r", " ").replace("\n", " "))

    lines = [
        "## Skill token counts", "", f"Tokenizer: {cell(encoding_name)}.", "",
        "| Skill | SKILL.md tokens | Supporting tokens | Total tokens |",
        "| --- | ---: | ---: | ---: |",
    ]
    for skill in skills:
        definition = skill["skill_md_tokens"]
        total = skill["total_tokens"]
        lines.append(f"| {cell(skill['skill'])} | {definition:,} | {total - definition:,} | {total:,} |")
    definitions = sum(skill["skill_md_tokens"] for skill in skills)
    total = sum(skill["total_tokens"] for skill in skills)
    lines += [
        f"| **Total** | **{definitions:,}** | **{total - definitions:,}** | **{total:,}** |",
        "", "Source-text counts; actual context usage depends on which files the host loads.",
    ]
    for skill in skills:
        if skill["skipped_files"]:
            paths = ", ".join(cell(path) for path in skill["skipped_files"])
            lines += ["", f"Skipped non-text files in {cell(skill['skill'])}: {paths}"]
    return "\n".join(lines)


def count_skills(root, encoding, include_supporting=False):
    """Count files independently, preserving whitespace and treating special tokens as text."""
    skills = []
    definitions = sorted(
        path for path in root.rglob("SKILL.md")
        if not any(part.startswith(".") or part == "__pycache__"
                   for part in path.relative_to(root).parts)
    )
    for definition in definitions:
        directory = definition.parent
        paths = [definition]
        if include_supporting:
            nested_packages = [path.parent for path in definitions
                               if path != definition and path.is_relative_to(directory)]
            paths += sorted(
                path for path in directory.rglob("*")
                if path != definition and path.is_file()
                and not any(part.startswith(".") or part == "__pycache__"
                            for part in path.relative_to(directory).parts)
                and not any(path.is_relative_to(package) for package in nested_packages)
            )
        files = []
        skipped = []
        for path in paths:
            # Do not follow supporting-file symlinks outside the skill package.
            if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
                raise ValueError(f"Symlink or external file in skill: {path}")
            data = path.read_bytes()
            try:
                text = data.decode("utf-8")
                if b"\0" in data:
                    raise UnicodeError("binary file")
            except UnicodeError:
                if path == definition:
                    raise ValueError(f"SKILL.md must be UTF-8 text: {path}") from None
                skipped.append(path.relative_to(directory).as_posix())
                continue
            files.append({
                "path": path.relative_to(directory).as_posix(),
                "tokens": len(encoding.encode_ordinary(text)),
            })
        skills.append({
            "skill": directory.relative_to(root).as_posix(),
            "skill_md_tokens": files[0]["tokens"],
            "total_tokens": sum(file["tokens"] for file in files),
            "files": files,
            "skipped_files": skipped,
        })
    return skills


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR,
                        help="Directory containing skill directories (default: this repo's skills/)")
    parser.add_argument("--encoding", default="o200k_base",
                        help="tiktoken encoding name (default: o200k_base)")
    parser.add_argument("--include-supporting", action="store_true",
                        help="Also count non-hidden UTF-8 text files within each skill")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="Output a JSON report")
    output.add_argument("--markdown", action="store_true", help="Output a Markdown summary table")
    args = parser.parse_args()
    if not args.skills_dir.is_dir():
        parser.error(f"Not a directory: {args.skills_dir}")
    try:
        encoding = tiktoken.get_encoding(args.encoding)
        skills = count_skills(args.skills_dir, encoding, args.include_supporting)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if not skills:
        parser.error(f"No SKILL.md files found recursively in {args.skills_dir}")
    total = sum(skill["total_tokens"] for skill in skills)
    if args.json:
        print(json.dumps({
            "encoding": encoding.name,
            "include_supporting": args.include_supporting,
            "skills": skills,
            "total_tokens": total,
        }, indent=2))
    elif args.markdown:
        print(markdown_report(skills, encoding.name))
    else:
        print(f"Encoding: {encoding.name}\n")
        width = max(len("Skill"), *(len(skill["skill"]) for skill in skills))
        print(f"{'Skill':<{width}}  {'SKILL.md':>10}  {'Total':>10}")
        for skill in skills:
            print(f"{skill['skill']:<{width}}  {skill['skill_md_tokens']:>10,}"
                  f"  {skill['total_tokens']:>10,}")
            if skill["skipped_files"]:
                print(f"  Skipped non-text files: {', '.join(skill['skipped_files'])}")
        print(f"\nTotal: {total:,} tokens")


if __name__ == "__main__":
    main()
