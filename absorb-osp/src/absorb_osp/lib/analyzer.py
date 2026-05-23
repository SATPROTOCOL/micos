"""absorb-osp — Project Analyzer (GitHub metadata, tech stack, security)"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from .models import ProjectInfo


def parse_github_url(url: str) -> tuple[str, str]:
    """Parse a GitHub URL into owner and repo name."""
    url = url.strip().rstrip("/")
    # Handle various URL formats
    patterns = [
        r"github\.com/([^/]+)/([^/]+)",
        r"git@github\.com:([^/]+)/([^/]+)",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            owner = m.group(1)
            repo = m.group(2).replace(".git", "")
            return owner, repo
    raise ValueError(f"Invalid GitHub URL: {url}")


def analyze_github_url(url: str) -> ProjectInfo:
    """Analyze a GitHub URL to extract project metadata.

    Uses web fetch (via curl) to get GitHub API data if available,
    otherwise returns basic info from the URL.
    """
    owner, repo = parse_github_url(url)

    info = ProjectInfo(
        github_url=f"https://github.com/{owner}/{repo}",
        name=repo,
    )

    # Try GitHub API
    api_data = _fetch_github_api(owner, repo)
    if api_data:
        info.stars = api_data.get("stargazers_count", 0)
        info.license_type = (api_data.get("license") or {}).get("spdx_id", "Unknown")
        info.description = api_data.get("description", "")
        info.language = api_data.get("language", "")
        info.last_commit = api_data.get("updated_at", "")
        info.open_issues = api_data.get("open_issues_count", 0)
        info.contributors = _count_contributors(owner, repo)

    return info


def _fetch_github_api(owner: str, repo: str) -> Optional[dict]:
    """Fetch project data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "id" in data:
                return data
    except Exception:
        pass
    return None


def _count_contributors(owner: str, repo: str) -> int:
    """Count contributors via GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
    try:
        result = subprocess.run(
            ["curl", "-s", "-I", url],
            capture_output=True, text=True, timeout=10
        )
        # Parse Link header for last page
        m = re.search(r'page=(\d+)>; rel="last"', result.stdout)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 0


def detect_tech_stack(path: str) -> dict:
    """Detect technology stack from a project directory."""
    tech = {
        "language": None,
        "framework": None,
        "build_system": None,
        "dependencies": [],
        "has_docker": False,
        "has_ci": False,
    }

    p = Path(path)
    if not p.exists():
        return tech

    # Language detection
    if (p / "Cargo.toml").exists():
        tech["language"] = "Rust"
        tech["build_system"] = "cargo"
    elif (p / "go.mod").exists():
        tech["language"] = "Go"
        tech["build_system"] = "go"
    elif (p / "package.json").exists():
        tech["language"] = "JavaScript/TypeScript"
        tech["build_system"] = "npm"
        tech["framework"] = _detect_js_framework(p)
    elif (p / "pyproject.toml").exists() or (p / "setup.py").exists():
        tech["language"] = "Python"
        tech["build_system"] = "pip"
    elif (p / "pom.xml").exists() or (p / "build.gradle").exists():
        tech["language"] = "Java"
        tech["build_system"] = "maven" if (p / "pom.xml").exists() else "gradle"

    # Docker
    if (p / "Dockerfile").exists():
        tech["has_docker"] = True

    # CI
    if (p / ".github" / "workflows").exists():
        tech["has_ci"] = True

    return tech


def _detect_js_framework(path: Path) -> Optional[str]:
    """Detect JavaScript framework from package.json."""
    pkg_file = path / "package.json"
    if not pkg_file.exists():
        return None
    try:
        data = json.loads(pkg_file.read_text())
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "next" in deps:
            return "Next.js"
        if "react" in deps:
            return "React"
        if "vue" in deps:
            return "Vue"
        if "svelte" in deps:
            return "Svelte"
    except Exception:
        pass
    return None
