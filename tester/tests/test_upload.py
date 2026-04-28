import sys
from io import BytesIO

import requests


APP_URL = "http://app:5000"
UPLOAD_URL = f"{APP_URL}/upload"
TEST_FILENAME = "test_upload_file.txt"
TEST_CONTENT = b"DevOps upload test content"


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    files = {
        "file": (TEST_FILENAME, BytesIO(TEST_CONTENT), "text/plain")
    }

    response = requests.post(UPLOAD_URL, files=files, timeout=10)

    if response.status_code != 200:
        fail(f"Expected status code 200, got {response.status_code}")

    try:
        response_data = response.json()
    except ValueError:
        fail("Upload response is not valid JSON")

    uploaded_files = response_data.get("files", [])

    if TEST_FILENAME not in uploaded_files:
        fail(
            f"Uploaded file '{TEST_FILENAME}' was not found in response: "
            f"{uploaded_files}"
        )

    print(f"Upload integration test passed: {TEST_FILENAME}")


if __name__ == "__main__":
    main()