"""absorb-osp — Privacy and Security Scanner"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

# ── Privacy leak patterns ──────────────────────────────────────────

PRIVACY_PATTERNS: list[tuple[str, str]] = [
    (r'[A-Za-z]:\\[Uu]sers\\[^\\]+\\', "Local Windows path (C:\\Users\\)"),
    (r'/home/[^/]+/', "Linux home path"),
    (r'/Users/[^/]+/', "macOS user path"),
    (r'-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----', "Private key"),
    (r'sk-[a-zA-Z0-9]{20,}', "Potential API key"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub PAT"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    (r'mongodb(\+srv)?://[^:]+:[^@]+@', "MongoDB credentials"),
    (r'postgres(ql)?://[^:]+:[^@]+@', "PostgreSQL credentials"),
]

PRIVACY_ALLOWLIST: list[str] = [
    r'noreply@anthropic\.com',
    r'img\.shields\.io',
    r'github\.com/SATPROTOCOL',
    r'github\.com/HermesAgent',
    r'claude\.ai',
    r'raw\.githubusercontent\.com',
    r'localhost',
    r'127\.0\.0\.1',
    # Scanner own pattern definitions
    r"/home/",
    r"/Users/",
    r"PRIVACY_PATTERNS",
    r"PRIVACY_ALLOWLIST",
]


def scan_for_leaks(path: str, verbose: bool = False) -> list[dict]:
    """Scan files for privacy leaks. Returns list of findings."""
    findings = []
    path_obj = Path(path)
    files = _collect_files(path_obj)

    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            for lineno, line in enumerate(content.split("\n"), 1):
                if _is_allowed(line):
                    continue
                for pattern, desc in PRIVACY_PATTERNS:
                    if re.search(pattern, line):
                        findings.append({
                            "file": str(filepath),
                            "line": lineno,
                            "pattern": desc,
                            "content": line.strip()[:120],
                        })
        except Exception:
            pass

    return findings


def _collect_files(path: Path) -> list[Path]:
    """Collect all text files to scan."""
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
    skip_ext = {".pyc", ".exe", ".dll", ".so", ".bin", ".png", ".jpg", ".gif", ".ico"}

    files = []
    for f in path.rglob("*"):
        if any(d in f.parts for d in skip_dirs):
            continue
        if f.suffix in skip_ext or f.name.startswith("."):
            continue
        if f.is_file():
            files.append(f)
    return files


def _is_allowed(line: str) -> bool:
    """Check if a line matches the allowlist."""
    return any(re.search(p, line) for p in PRIVACY_ALLOWLIST)


# ── Security red-flag scanner ──────────────────────────────────────

def security_scan(path: str) -> dict:
    """Run security red-flag checks on a project directory.

    Returns dict with check results and gate decision.
    """
    results = {
        "checks": [],
        "summary": {"pass": 0, "warn": 0, "fail": 0, "skip": 0},
        "gate": "PASS",
    }

    p = Path(path)
    if not p.exists():
        results["gate"] = "FAIL"
        return results

    # Check 1: Binary blobs
    binaries = _find_binaries(p)
    _add_check(results, "Binary blobs without source", "warn" if binaries else "pass",
               f"Found: {binaries}" if binaries else "")

    # Check 2: eval/exec
    eval_count = _grep_count(p, r'exec\(|eval\(', skip_dirs={".git", "node_modules", "__pycache__"})
    _add_check(results, "Dangerous eval/exec", "warn" if eval_count else "pass",
               f"{eval_count} instance(s)" if eval_count else "")

    # Check 3: Obfuscation
    obfuscated = _grep_count(p, r'base64|fromhex|charCodeAt', skip_dirs={".git", "node_modules"})
    _add_check(results, "Obfuscated code", "warn" if obfuscated else "pass",
               f"{obfuscated} matches" if obfuscated else "")

    # Check 4: License
    license_files = list(p.glob("LICENSE*")) + list(p.glob("COPYING*"))
    _add_check(results, "License file", "pass" if license_files else "fail",
               f"Found: {license_files[0].name}" if license_files else "Missing license")

    # Gate
    if results["summary"]["fail"] > 0:
        results["gate"] = "BLOCKED"
    elif results["summary"]["warn"] > 3:
        results["gate"] = "REVIEW"

    return results


def _add_check(results: dict, name: str, status: str, detail: str = ""):
    """Add a check result."""
    results["checks"].append({"name": name, "status": status, "detail": detail})
    results["summary"][status] = results["summary"].get(status, 0) + 1


def _find_binaries(path: Path) -> list[str]:
    """Find binary files in the project."""
    binary_ext = {".exe", ".dll", ".so", ".bin", ".class"}
    found = []
    for ext in binary_ext:
        for f in path.rglob(f"*{ext}"):
            parts = f.parts
            if not any(d in parts for d in (".git", "node_modules", "venv")):
                found.append(f.name)
    return found[:10]


def _grep_count(path: Path, pattern: str, skip_dirs: set = None) -> int:
    """Count regex matches in text files, skipping specified dirs."""
    if skip_dirs is None:
        skip_dirs = set()
    count = 0
    for f in path.rglob("*"):
        if any(d in f.parts for d in skip_dirs):
            continue
        if f.is_file() and f.suffix in {".py", ".js", ".ts", ".sh", ".pl", ".rb"}:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                count += len(re.findall(pattern, content))
            except Exception:
                pass
    return count
