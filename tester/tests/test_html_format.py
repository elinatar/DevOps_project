import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


APP_DIR = Path("/app")
SOURCE_TEMPLATES_DIR = APP_DIR / "templates"


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    if not SOURCE_TEMPLATES_DIR.exists():
        fail(f"Templates directory not found: {SOURCE_TEMPLATES_DIR}")

    html_files = list(SOURCE_TEMPLATES_DIR.glob("*.html"))

    if not html_files:
        fail("No HTML files found for formatting")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_templates_dir = Path(temp_dir) / "templates"
        shutil.copytree(SOURCE_TEMPLATES_DIR, temp_templates_dir)

        result = subprocess.run(
            [
                "python3",
                "/usr/local/bin/css-html-prettify.py",
                str(temp_templates_dir),
            ],
            text=True,
            capture_output=True,
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            fail("HTML formatting failed")

    print(f"HTML formatting passed for {len(html_files)} files")

if __name__ == "__main__":
    main()