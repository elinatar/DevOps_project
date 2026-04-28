import ast
import sys
from pathlib import Path


APP_DIR = Path("/app")
FORBIDDEN_VARIABLE_NAME = "elina"


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def check_file(path):
    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        fail(f"Cannot parse Python file {path}: {error}")

    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == FORBIDDEN_VARIABLE_NAME:
            violations.append((path, node.lineno, node.id))

    return violations


def main():
    python_files = list(APP_DIR.glob("*.py"))

    if not python_files:
        fail(f"No Python files found in {APP_DIR}")

    all_violations = []

    for path in python_files:
        all_violations.extend(check_file(path))

    if all_violations:
        for path, line, name in all_violations:
            print(
                f"Forbidden variable name '{name}' found in {path} "
                f"at line {line}",
                file=sys.stderr,
            )
        sys.exit(1)

    print(
        f"Custom static rule passed: variable name "
        f"'{FORBIDDEN_VARIABLE_NAME}' was not found"
    )


if __name__ == "__main__":
    main()