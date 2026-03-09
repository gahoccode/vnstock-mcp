#!/usr/bin/env python3
"""
PyPI Publishing Automation Script

This script automates the process of building and publishing the vnstock-mcp
package to PyPI. It loads the UV_PUBLISH_TOKEN from .env file.

Usage:
    python dev/publish.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def clean_build_artifacts() -> None:
    """Remove dist/ and *.egg-info directories."""
    project_root = Path(__file__).parent.parent

    # Clean dist/
    dist_dir = project_root / "dist"
    if dist_dir.exists():
        print(f"Removing {dist_dir}...")
        shutil.rmtree(dist_dir)

    # Clean *.egg-info directories
    for egg_info in project_root.glob("*.egg-info"):
        print(f"Removing {egg_info}...")
        shutil.rmtree(egg_info)


def run_command(cmd: list[str], env: dict[str, str] | None = None) -> None:
    """Run a shell command and exit on failure."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main() -> None:
    """Main publishing workflow."""
    # Load environment variables from .env
    load_dotenv()

    # Check for UV_PUBLISH_TOKEN
    publish_token = os.getenv("UV_PUBLISH_TOKEN")
    if not publish_token:
        print("Error: UV_PUBLISH_TOKEN not found in environment variables.")
        print("Please set UV_PUBLISH_TOKEN in your .env file.")
        sys.exit(1)

    print("Starting PyPI publishing process...\n")

    # Step 1: Clean build artifacts
    print("Step 1: Cleaning build artifacts...")
    clean_build_artifacts()
    print("Done.\n")

    # Step 2: Build the package
    print("Step 2: Building package...")
    run_command(["uv", "build"])
    print("Done.\n")

    # Step 3: Publish to PyPI
    print("Step 3: Publishing to PyPI...")
    env = os.environ.copy()
    env["UV_PUBLISH_TOKEN"] = publish_token
    run_command(["uv", "publish", "--token", publish_token], env=env)
    print("Done.\n")

    print("Publishing complete!")


if __name__ == "__main__":
    main()