import subprocess
import sys
import tempfile
from pathlib import Path


APP_DIR = "/app"


CHECKER_CODE = """
from pylint.checkers import BaseChecker


class ElinaVariableChecker(BaseChecker):
    name = "elina-variable-checker"

    msgs = {
        "C9001": (
            "Forbidden variable name 'elina'",
            "forbidden-elina-variable",
            "Used when a variable has the forbidden name 'elina'.",
        ),
    }

    def visit_assignname(self, node):
        if node.name == "elina":
            self.add_message("forbidden-elina-variable", node=node)


def register(linter):
    linter.register_checker(ElinaVariableChecker(linter))
"""


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        checker_path = Path(temp_dir) / "pylint_elina_checker.py"
        checker_path.write_text(CHECKER_CODE, encoding="utf-8")

        result = subprocess.run(
            [
                "pylint",
                f"--init-hook=import sys; sys.path.insert(0, '{temp_dir}')",
                "--load-plugins=pylint_elina_checker",
                "--disable=all",
                "--enable=forbidden-elina-variable",
                APP_DIR,
            ],
            text=True,
            capture_output=True,
        )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if "forbidden-elina-variable" in result.stdout:
        fail("Custom pylint rule failed: forbidden variable name 'elina' was found")

    if result.returncode not in (0, 16):
        fail(f"pylint finished with unexpected return code {result.returncode}")

    print("Custom pylint rule passed: variable name 'elina' was not found")


if __name__ == "__main__":
    main()