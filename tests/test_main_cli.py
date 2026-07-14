import subprocess
import sys
import unittest
from pathlib import Path

from src.main import app


class MainCliTests(unittest.TestCase):
    def test_main_cli_starts_with_exit_option(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            cwd=repo_root,
            input="0\n",
            text=True,
            capture_output=True,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("NOVA v0.1", result.stdout)


if __name__ == "__main__":
    unittest.main()
