import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
STDOUT_LOG = LOG_DIR / "stdout.log"
STDERR_LOG = LOG_DIR / "stderr.log"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_stdout(message):
    line = f"[{timestamp()}] {message}"
    print(line)

    # запись в файл
    with STDOUT_LOG.open("a", encoding="utf-8") as file:
        file.write(line + "\n")

    # запись в docker logs
    try:
        with open("/proc/1/fd/1", "a") as docker_out:
            docker_out.write(line + "\n")
    except Exception:
        pass


def write_stderr(message):
    line = f"[{timestamp()}] {message}"
    print(line, file=sys.stderr)

    # запись в файл
    with STDERR_LOG.open("a", encoding="utf-8") as file:
        file.write(line + "\n")

    # запись в docker logs
    try:
        with open("/proc/1/fd/2", "a") as docker_err:
            docker_err.write(line + "\n")
    except Exception:
        pass


def run_step(name, command):
    write_stdout(f"START: {name}")

    result = subprocess.run(
        command,
        shell=True,
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        for line in result.stdout.splitlines():
            write_stdout(f"{name}: {line}")

    if result.stderr:
        for line in result.stderr.splitlines():
            write_stderr(f"{name}: {line}")

    if result.returncode == 0:
        write_stdout(f"SUCCESS: {name}")
        return True

    write_stderr(f"FAIL: {name} with exit code {result.returncode}")
    return False


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    STDOUT_LOG.write_text("", encoding="utf-8")
    STDERR_LOG.write_text("", encoding="utf-8")

    steps = [
        ("HTML formatting test", "python3 tests/test_html_format.py"),
        ("Custom rule test", "python3 tests/test_custom_rule.py"),
        ("Upload test", "python3 tests/test_upload.py"),
    ]

    all_passed = True

    for name, command in steps:
        if not run_step(name, command):
            all_passed = False

    if all_passed:
        write_stdout("ALL TESTS PASSED")
        sys.exit(0)

    write_stderr("SOME TESTS FAILED")
    sys.exit(1)


if __name__ == "__main__":
    main()