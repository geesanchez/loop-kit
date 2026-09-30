"""Regression budgets for the shipped kit and its unfilled context templates.

These limits measure recurring startup text, not a maximum size for a user's
project context. Characters are counted from exact UTF-8 text (including line
endings); characters / 4 is only a rough token estimate, never tokenization.
One host entry point is loaded, so AGENTS.md is counted once and CLAUDE.md is
checked separately as an identical alternative.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ("AGENTS.md", "LOOP.md", "context/RULES.md")
MAKER_STARTUP = INSTRUCTIONS + (
    "context/VISION.md",
    "context/ARCHITECTURE.md",
    "memory/PROGRESS.md",
)


class ContextBudgetTests(unittest.TestCase):
    def assert_character_budget(self, paths, budget):
        # Decode bytes directly so universal-newline translation cannot hide
        # characters in the actual files. No tokenizer or dependency is needed.
        contributions = {
            path: len((ROOT / path).read_bytes().decode("utf-8"))
            for path in paths
        }
        total = sum(contributions.values())
        details = "\n".join(
            f"  {path}: {count:,} characters; {count / 4:,.2f} estimated tokens"
            for path, count in contributions.items()
        )
        self.assertLessEqual(
            total,
            budget,
            f"Shipped-kit budget exceeded: {total:,} characters > {budget:,}.\n"
            f"Per-file contributions:\n{details}\n"
            f"Total: {total:,} characters; {total / 4:,.2f} estimated tokens.\n"
            "All token estimates are characters / 4, not measured model tokens.",
        )

    def test_recurring_instructions_fit_5000_characters(self):
        self.assert_character_budget(INSTRUCTIONS, 5000)

    def test_full_maker_startup_fits_8500_characters(self):
        self.assert_character_budget(MAKER_STARTUP, 8500)

    def test_active_memory_fits_1800_characters(self):
        self.assert_character_budget(("memory/PROGRESS.md",), 1800)

    def test_host_entry_points_are_byte_identical(self):
        self.assertTrue(
            (ROOT / "AGENTS.md").read_bytes() == (ROOT / "CLAUDE.md").read_bytes(),
            "AGENTS.md and CLAUDE.md must be byte-identical host entry points.",
        )


if __name__ == "__main__":
    unittest.main()
