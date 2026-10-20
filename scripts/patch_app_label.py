
#!/usr/bin/env python3
"""Safely change the Android app display label when the resource exists."""

from pathlib import Path
import re
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 patch_app_label.py <android-project-directory>")
        return 2

    project = Path(sys.argv[1]).resolve()

    if not project.is_dir():
        print(f"ERROR: Project directory does not exist: {project}")
        return 2

    candidates = list(
        project.glob("app/src/main/res/values/strings.xml")
    )

    if not candidates:
        print("WARNING: strings.xml not found; no changes made.")
        return 0

    pattern = re.compile(
        r"""(<string\b[^>]*\bname=["']app_name["'][^>]*>).*?(</string>)""",
        re.DOTALL,
    )

    for path in candidates:
        original = path.read_text(encoding="utf-8")

        updated, count = pattern.subn(
            r"\1GoldenEye 007\2",
            original,
            count=1,
        )

        if count:
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                print(f"SUCCESS: Updated app label in {path}")
            else:
                print("SUCCESS: App label is already GoldenEye 007.")
            return 0

    print("WARNING: app_name resource not found; no changes made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
