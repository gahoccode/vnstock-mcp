from importlib import metadata
from unittest.mock import MagicMock, patch

import pytest
from starlette.responses import JSONResponse

from vnstock_mcp.server import health_check
from vnstock_mcp.version import (
    get_distribution_version,
    get_git_tag,
    get_package_version,
    get_runtime_version,
)


class TestVersionHelpers:
    """Tests for runtime and package version helpers."""

    def test_get_git_tag_exact_match(self):
        """Exact HEAD tag should be returned when git metadata is available."""
        completed = MagicMock(stdout="v0.4.0\n")

        with patch("vnstock_mcp.version.subprocess.run", return_value=completed):
            assert get_git_tag() == "v0.4.0"

    def test_get_runtime_version_prefers_git_tag(self):
        """Runtime version should prefer the exact git tag."""
        completed = MagicMock(stdout="v0.4.0\n")

        with (
            patch("vnstock_mcp.version.subprocess.run", return_value=completed),
            patch("vnstock_mcp.version.os.getenv", return_value=None),
            patch("vnstock_mcp.version.metadata.version", return_value="0.4.0"),
        ):
            assert get_runtime_version() == "v0.4.0"

    def test_get_runtime_version_env_fallback(self):
        """Environment variable should be used when git metadata is absent."""
        with (
            patch("vnstock_mcp.version.subprocess.run", side_effect=FileNotFoundError()),
            patch("vnstock_mcp.version.os.getenv", return_value="v0.4.0"),
            patch("vnstock_mcp.version.metadata.version", return_value="0.4.0"),
        ):
            assert get_runtime_version() == "v0.4.0"

    def test_get_runtime_version_package_fallback(self):
        """Installed package metadata should be the next fallback."""
        with (
            patch("vnstock_mcp.version.subprocess.run", side_effect=FileNotFoundError()),
            patch("vnstock_mcp.version.os.getenv", return_value=None),
            patch("vnstock_mcp.version.metadata.version", return_value="0.4.0"),
        ):
            assert get_runtime_version() == "0.4.0"

    def test_get_runtime_version_unknown(self):
        """Runtime version should degrade to unknown when nothing is available."""
        with (
            patch("vnstock_mcp.version.subprocess.run", side_effect=FileNotFoundError()),
            patch("vnstock_mcp.version.os.getenv", return_value=None),
            patch(
                "vnstock_mcp.version.metadata.version",
                side_effect=metadata.PackageNotFoundError,
            ),
        ):
            assert get_runtime_version() == "unknown"

    def test_get_distribution_version_normalizes_git_tag(self):
        """Package metadata should strip the release tag prefix when needed."""
        completed = MagicMock(stdout="v0.4.0\n")

        with (
            patch(
                "vnstock_mcp.version.metadata.version",
                side_effect=metadata.PackageNotFoundError,
            ),
            patch("vnstock_mcp.version.subprocess.run", return_value=completed),
            patch("vnstock_mcp.version.os.getenv", return_value=None),
        ):
            assert get_distribution_version() == "0.4.0"

    def test_get_package_version(self):
        """Package metadata should be read from importlib.metadata."""
        with patch("vnstock_mcp.version.metadata.version", return_value="0.4.0"):
            assert get_package_version() == "0.4.0"


@pytest.mark.asyncio
async def test_health_check_uses_runtime_version():
    """Health endpoint should surface the dynamically resolved version."""
    with patch("vnstock_mcp.server.get_runtime_version", return_value="v0.4.0"):
        response = await health_check(MagicMock())

    assert isinstance(response, JSONResponse)
    assert b'"version":"v0.4.0"' in response.body
