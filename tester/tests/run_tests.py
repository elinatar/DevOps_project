import subprocess
import sys
from datetime import datetime


def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def run_step(name, command):
    log(f"START: {name}")
    try:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            log(f"FAIL: {name}")
            return False
        log(f"SUCCESS: {name}")
        return True
    except Exception as e:
        log(f"ERROR: {name} -> {e}")
        return False


def main():
    steps = [
        ("HTML formatting test", "python3 tests/test_html_format.py"),
        ("Custom rule test", "python3 tests/test_custom_rule.py"),
        ("Upload test", "python3 tests/test_upload.py"),
    ]

    success = True

    for name, command in steps:
        result = run_step(name, command)
        if not result:
            success = False

    if success:
        log("ALL TESTS PASSED")
        sys.exit(0)
    else:
        log("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
