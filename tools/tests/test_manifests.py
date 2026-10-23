"""Tests for the plugin's own component files: every agent and skill opens with frontmatter that a
strict YAML parser accepts. An unquoted ": " inside a plain value makes Claude Code load the file with
empty metadata (no allowed-tools, no preloaded skills), so it is caught here.
No network. Run: python3 -I -m unittest discover -s tools/tests -p "test_*.py"
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPONENTS = sorted(ROOT.glob("agents/*.md")) + sorted(ROOT.glob("skills/*/SKILL.md"))


def frontmatter_lines(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    out = []
    for line in lines[1:]:
        if line == "---":
            return out
        out.append(line)
    return None


class TestFrontmatter(unittest.TestCase):
    def test_components_exist(self):
        self.assertGreaterEqual(len(list(ROOT.glob("agents/*.md"))), 9)
        self.assertGreaterEqual(len(list(ROOT.glob("skills/*/SKILL.md"))), 20)

    def test_frontmatter_is_closed_and_named(self):
        for path in COMPONENTS:
            fm = frontmatter_lines(path)
            self.assertIsNotNone(fm, "%s: frontmatter missing or not closed" % path)
            keys = [ln.split(":", 1)[0] for ln in fm if re.match(r"^[a-z][a-z-]*:", ln)]
            self.assertIn("name", keys, path)
            self.assertIn("description", keys, path)

    def test_plain_values_have_no_colon_space(self):
        for path in COMPONENTS:
            for line in frontmatter_lines(path) or []:
                m = re.match(r"^([a-z][a-z-]*):\s*(.*)$", line)
                if not m:
                    continue
                value = m.group(2)
                if value.startswith(('"', "'")):
                    self.assertTrue(value.endswith(value[0]) and len(value) > 1,
                                    "%s: %s is not a closed quoted string" % (path, m.group(1)))
                    continue
                self.assertNotIn(": ", value, "%s: quote the %s value; ': ' breaks YAML" % (path, m.group(1)))
                self.assertFalse(value.startswith(("[", "{", "*", "&", "!", "%", "@", "`")) and m.group(1) == "description",
                                 "%s: description starts with a YAML indicator" % path)


if __name__ == "__main__":
    unittest.main()
