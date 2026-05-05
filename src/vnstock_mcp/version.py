"""Version helpers for VNStock MCP Server."""

from __future__ import annotations

import os
import subprocess
from importlib import metadata
from pathlib import Path

_DISTRIBUTION_NAME = "vnstock-mcp"


def _repo_root() -> Path:
    """Return the repository root for git-based version detection."""
    return Path(__file__).resolve().parents[2]


def _normalize_version(value: str) -> str:
    """Normalize tag-like values to package-version form."""
    if value.startswith("v") and len(value) > 1 and value[1].isdigit():
        return value[1:]
    return value


def get_git_tag() -> str | None:
    """Return the exact git tag for HEAD when the repository is tagged."""
    try:
        completed = subprocess.run(
            ["git", "describe", "--tags", "--exact-match", "HEAD"],
            cwd=_repo_root(),
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        return None

    tag = completed.stdout.strip()
    return tag or None


def get_package_version() -> str | None:
    """Return the installed package version if metadata is available."""
    try:
        return metadata.version(_DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError:
        return None


def get_runtime_version() -> str:
    """Return the version exposed by the health endpoint."""
    return (
        get_git_tag()
        or os.getenv("VNSTOCK_MCP_VERSION")
        or get_package_version()
        or "unknown"
    )


def get_distribution_version() -> str:
    """Return the package version used for module metadata."""
    return _normalize_version(
        get_package_version()
        or get_git_tag()
        or os.getenv("VNSTOCK_MCP_VERSION")
        or "unknown"
    )
