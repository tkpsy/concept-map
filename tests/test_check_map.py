"""Exercise map invariants and the complete map shown in the documentation."""

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_map.py"
spec = importlib.util.spec_from_file_location("check_map", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class MapCheckTests(unittest.TestCase):
    def check_files(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for name, content in files.items():
                path = directory / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return checker.check(directory)

    def test_single_root(self):
        self.assertEqual(self.check_files({"root.md": "# root"}), ([], "root", 1, 0))

    def test_complete_documentation_example(self):
        reference = (ROOT / "references/auth-example.md").read_text(encoding="utf-8")
        files = dict(re.findall(r"^#### ([^\n]+\.md)\n\n```markdown\n(.*?)\n```", reference, re.M | re.S))
        self.assertEqual(len(files), 5)
        self.assertEqual(self.check_files(files), ([], "タスク管理アプリ", 5, 4))

    def test_duplicate_mentions_code_and_unimplemented_node(self):
        files = {
            "root.md": "[[子]] [[子]]\n`[[inline]]`\n```md\n[[fenced]]\n```\n",
            "子.md": "# 子\n未実装。",
        }
        self.assertEqual(self.check_files(files), ([], "root", 2, 1))

    def test_missing_target(self):
        errors, _, _, _ = self.check_files({"root.md": "[[missing]]"})
        self.assertTrue(any("リンク切れ" in error for error in errors))

    def test_multiple_parents(self):
        files = {"root.md": "[[a]] [[b]]", "a.md": "[[c]]", "b.md": "[[c]]", "c.md": "# c"}
        errors, _, _, _ = self.check_files(files)
        self.assertTrue(any("親が複数" in error for error in errors))

    def test_disconnected_cycle_with_n_minus_one_edges(self):
        files = {"root.md": "[[a]]", "a.md": "# a", "b.md": "[[c]]", "c.md": "[[b]]"}
        errors, _, nodes, edges = self.check_files(files)
        self.assertEqual(edges, nodes - 1)
        self.assertTrue(any("循環" in error for error in errors))
        self.assertTrue(any("到達できません" in error for error in errors))

    def test_multiple_roots(self):
        errors, root, _, _ = self.check_files({"a.md": "# a", "b.md": "# b"})
        self.assertIsNone(root)
        self.assertTrue(any("root は一つ" in error for error in errors))

    def test_self_link(self):
        errors, _, _, _ = self.check_files({"a.md": "[[a]]"})
        self.assertTrue(any("循環" in error for error in errors))

    def test_nested_node(self):
        errors, _, _, _ = self.check_files({"root.md": "# root", "nested/child.md": "# child"})
        self.assertTrue(any("直下" in error for error in errors))

    def test_empty_map(self):
        errors, _, nodes, _ = self.check_files({})
        self.assertTrue(errors)
        self.assertEqual(nodes, 0)

    def test_command_line_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "root.md"
            path.write_text("# root", encoding="utf-8")
            good = subprocess.run([sys.executable, str(SCRIPT), tmp], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            path.write_text("[[missing]]", encoding="utf-8")
            bad = subprocess.run([sys.executable, str(SCRIPT), tmp], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1, bad.stderr)


if __name__ == "__main__":
    unittest.main()
