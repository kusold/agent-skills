"""Run: uv run --with tiktoken==0.12.0 python -m unittest discover -s scripts"""

import tempfile
import unittest
from pathlib import Path

import tiktoken

from count_skill_tokens import count_skills, markdown_report


class TokenCounts(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.encoding = tiktoken.get_encoding("o200k_base")

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target

    def test_counts_complete_source_and_ignores_supporting_by_default(self):
        source = "---\r\nname: example\r\n---\r\n# 研究\r\n<|endoftext|>\r\n"
        self.write("example/SKILL.md", source.encode())
        self.write("example/references/notes.md", b"Supporting notes")
        self.write("not-a-skill/notes.md", b"Ignored")
        skills = count_skills(self.root, self.encoding)
        self.assertEqual(len(skills), 1)
        self.assertEqual(skills[0]["total_tokens"],
                         len(self.encoding.encode(source, disallowed_special=())))
        self.assertEqual(len(skills[0]["files"]), 1)

    def test_supporting_files_are_counted_individually_and_binary_is_reported(self):
        self.write("example/SKILL.md", b"hello")
        self.write("example/references/notes.md", b" world")
        self.write("example/scripts/run.py", b"print('hello')\n")
        self.write("example/image.png", b"\x89PNG\xff")
        self.write("example/null.bin", b"a\0b")
        self.write("example/.hidden", b"Ignored")
        self.write("example/__pycache__/cache.pyc", b"Ignored")
        skill = count_skills(self.root, self.encoding, True)[0]
        expected = sum(len(self.encoding.encode_ordinary(text))
                       for text in ["hello", " world", "print('hello')\n"])
        self.assertEqual(skill["total_tokens"], expected)
        self.assertEqual(len(skill["files"]), 3)
        self.assertEqual(skill["skipped_files"], ["image.png", "null.bin"])

    def test_invalid_definition_fails_instead_of_undercounting(self):
        self.write("broken/SKILL.md", b"\xff")
        with self.assertRaisesRegex(ValueError, "must be UTF-8"):
            count_skills(self.root, self.encoding)

    def test_grouped_skills_have_distinct_relative_paths(self):
        self.write("flat/SKILL.md", b"Flat skill")
        self.write("llm-wiki/wiki-query/SKILL.md", b"Wiki skill")
        self.write("languages/nix/example/SKILL.md", b"Nix skill")
        self.write("other/example/SKILL.md", b"Other skill")
        self.write(".hidden/ignored/SKILL.md", b"Ignored")
        skills = count_skills(self.root, self.encoding)
        self.assertEqual([skill["skill"] for skill in skills], [
            "flat", "languages/nix/example", "llm-wiki/wiki-query", "other/example",
        ])

    def test_nested_packages_are_not_counted_as_parent_support(self):
        self.write("parent/SKILL.md", b"Parent")
        self.write("parent/notes.md", b"Supporting notes")
        self.write("parent/child/SKILL.md", b"Child")
        self.write("parent/child/notes.md", b"Child notes")
        parent, child = count_skills(self.root, self.encoding, True)
        self.assertEqual(parent["skill"], "parent")
        self.assertEqual(child["skill"], "parent/child")
        for skill in (parent, child):
            self.assertEqual([file["path"] for file in skill["files"]],
                             ["SKILL.md", "notes.md"])

    def test_markdown_has_per_skill_counts_totals_and_escaped_names(self):
        report = markdown_report([
            {"skill": "a|b<script>", "skill_md_tokens": 1000,
             "total_tokens": 1200, "skipped_files": ["image.png"]},
            {"skill": "second", "skill_md_tokens": 20,
             "total_tokens": 20, "skipped_files": []},
        ], "o200k_base")
        self.assertIn("| a&#124;b&lt;script&gt; | 1,000 | 200 | 1,200 |", report)
        self.assertIn("| second | 20 | 0 | 20 |", report)
        self.assertIn("| **Total** | **1,020** | **200** | **1,220** |", report)
        self.assertIn("Tokenizer: o200k_base.", report)
        self.assertIn("Skipped non-text files in a&#124;b&lt;script&gt;: image.png", report)

    def test_symlink_to_external_supporting_file_fails(self):
        self.write("example/SKILL.md", b"hello")
        external = self.write("external.md", b"outside")
        (self.root / "example" / "link.md").symlink_to(external)
        with self.assertRaisesRegex(ValueError, "Symlink or external"):
            count_skills(self.root, self.encoding, True)


if __name__ == "__main__":
    unittest.main()
