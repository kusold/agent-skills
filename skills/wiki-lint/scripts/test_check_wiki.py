"""Regression tests use disposable wikis and never touch real knowledge bases."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check_wiki.py")
SPEC = importlib.util.spec_from_file_location("check_wiki", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WikiChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "raw").mkdir()
        self.write("wiki/index.md", "# Index\n")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def findings(self, kind, **kwargs):
        return [f for f in MODULE.check(self.root, **kwargs) if f["kind"] == kind]

    def test_qualified_targets_do_not_fall_back_to_basename(self):
        self.write("wiki/sources/acme.md", "# Acme\n")
        self.write("wiki/index.md", "[[entities/acme]]\n")
        broken = self.findings("broken-wikilink")
        self.assertEqual([f["message"] for f in broken], ["[[entities/acme]]"])
        self.assertEqual(self.findings("index-missing-page")[0]["file"], "wiki/sources/acme.md")

    def test_index_keeps_distinct_pages_and_reports_ambiguity(self):
        self.write("wiki/entities/acme.md", "# Acme\n")
        self.write("wiki/sources/acme.md", "# Acme source\n")
        self.write("wiki/index.md", "[[entities/acme]]\n[[acme]]\n")
        self.assertEqual(self.findings("index-missing-page")[0]["file"], "wiki/sources/acme.md")
        self.assertEqual(len(self.findings("ambiguous-wikilink")), 1)

    def test_orphan_matching_requires_the_whole_target(self):
        self.write("wiki/concepts/data.md", "# Data\n")
        self.write("wiki/concepts/metadata.md", "# Metadata\n[[metadata]]\n")
        self.write("wiki/index.md", "[[concepts/data]]\n[[concepts/metadata]]\n")
        self.write("wiki/sources/article.md", "[[concepts/metadata]]\n")
        orphans = {f["file"] for f in self.findings("orphan")}
        self.assertIn("wiki/concepts/data.md", orphans)
        self.assertNotIn("wiki/concepts/metadata.md", orphans)

    def test_relative_raw_paths_spaces_unicode_and_url_encoding(self):
        self.write("raw/My Paper.pdf", "paper")
        self.write("raw/研究 notes.pdf", "paper")
        self.write("wiki/sources/paper.md", "\n".join([
            "[paper](../../raw/My%20Paper.pdf)",
            "[unicode](<../../raw/研究 notes.pdf>)",
            "[missing](../../raw/Not%20Here.pdf)",
        ]))
        broken = self.findings("broken-raw-reference")
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0]["line"], 3)
        self.assertIn("Not Here.pdf", broken[0]["message"])
        self.assertEqual(self.findings("unreferenced-raw"), [])

    def test_raw_frontmatter_and_inline_paths(self):
        self.write("raw/My Paper.pdf", "paper")
        self.write("raw/研究 notes.pdf", "paper")
        self.write("wiki/sources/a.md", '---\nsource: raw/My Paper.pdf\n---\n`raw/研究 notes.pdf`\n')
        self.assertEqual(self.findings("broken-raw-reference"), [])
        self.assertEqual(self.findings("unreferenced-raw"), [])

    def test_alias_anchor_extension_and_relative_wikilinks(self):
        self.write("wiki/entities/acme.md", "# Acme\n[[../sources/acme.md#Section|source]]\n")
        self.write("wiki/sources/acme.md", "# Acme source\n[[#Heading]]\n")
        self.write("wiki/index.md", "[[entities/acme.md|Acme]]\n[[sources/acme#Section]]\n")
        self.assertEqual(self.findings("broken-wikilink"), [])
        self.assertEqual(self.findings("index-missing-page"), [])
        self.assertNotIn("wiki/sources/acme.md", [f["file"] for f in self.findings("orphan")])

    def test_code_examples_do_not_create_link_findings(self):
        self.write("wiki/index.md", "# Index\n```md\n[[nonexistent]]\n```\n`[[also-absent]]`\n<!-- [[comment]] -->\n")
        self.assertEqual(self.findings("broken-wikilink"), [])

    def test_custom_paths_and_no_writes(self):
        self.write("material/研究.pdf", "paper")
        self.write("knowledge/catalog.md", "[[topics/research]]\n")
        self.write("knowledge/topics/research.md", "[research](../../material/研究.pdf)\n")
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        results = MODULE.check(self.root, "knowledge", "material", "knowledge/catalog.md")
        self.assertFalse(any(f["kind"] in {"broken-wikilink", "broken-raw-reference", "unreferenced-raw", "index-missing-page"} for f in results))
        after = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_cli_rejects_missing_layout_without_creating_files(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.root), "--index", "missing.md"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must exist", result.stderr)
        self.assertFalse((self.root / "missing.md").exists())


if __name__ == "__main__":
    unittest.main()
