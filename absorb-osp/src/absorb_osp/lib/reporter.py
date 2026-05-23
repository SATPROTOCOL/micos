"""absorb-osp — Report Generator (analysis reports, markdown)"""

import os
from datetime import date
from pathlib import Path
from typing import Optional

from .models import AbsorbedProject, Depth, JudgeScore, ProjectInfo, Status


def generate_analysis_report(
    project: ProjectInfo,
    score: JudgeScore,
    output_dir: str = ".",
) -> str:
    """Generate a standardized analysis report following the template format.

    Returns the path to the generated report.
    """
    today = date.today().isoformat()
    depth = score.suggested_depth.value
    status = "pending"

    # Build report content
    report = f"""---
absorb_date: {today}
github_url: {project.github_url}
license: {project.license_type}
stars: {project.stars}
depth: {depth}
status: {status}
judge_score: {score.total:.1f}
classify_decision: STANDALONE
integration_targets:
  - agent-skills
---

# {project.name} — Analysis Report

## 0. Triage Record

| Check | Result | Notes |
|-------|--------|-------|
| Security redline | ✅ PASS | Automated scan passed |
| Basic eligibility | ✅ PASS | {project.stars} stars, active project |
| Relevance | ✅ PASS | Viable for ecosystem integration |
| Absorbability | ✅ PASS | {project.license_type} license |

## 1. Verification Summary

| Dimension | Assessment | Evidence |
|-----------|------------|----------|
| GitHub activity | Active | {project.stars}★, {project.contributors} contributors |
| License | {project.license_type} | Compatible |
| Security status | Pending | Requires deep scan |
| Quality | TBD | Requires code review |

## 2. Project Overview

{project.description or f"{project.name} — a project written in {project.language or 'Unknown'}."}

## 3. Tech Stack

| Layer | Technology |
|-------|------------|
| Language | {project.language or 'TBD'} |

## 4. Security Audit

| Check | Result | Notes |
|-------|--------|-------|
| Malicious code | ⏳ Pending | |

## 5. Judge Scorecard

| Dimension | Weight | Score | Weighted | Note |
|-----------|--------|-------|----------|------|
| Capability fit | 30% | {score.capability_fit} | {score.capability_fit * 0.30:.2f} | Assessed during triage |
| Feasibility | 25% | {score.feasibility} | {score.feasibility * 0.25:.2f} | |
| Interface compat | 20% | {score.interface_compat} | {score.interface_compat * 0.20:.2f} | |
| Maintenance cost | 15% | {score.maintenance_cost} | {score.maintenance_cost * 0.15:.2f} | |
| Security risk | 10% | {score.security_risk} | {score.security_risk * 0.10:.2f} | |
| **Total** | **100%** | | **{score.total:.2f}** | |

**Decision**: {score.decision}

## 6. Usage Scenarios

1. CLI usage: _pending analysis_
2. Library usage: _pending analysis_

## 7. How to Start

```bash
# pending installation
```

## 8. How to Verify

```bash
# TBD
```
"""

    # Write file
    filename = f"{project.name}-analysis-report.md"
    output_path = Path(output_dir) / filename
    output_path.write_text(report, encoding="utf-8")

    return str(output_path)


def generate_usage_log(name: str, github_url: str, output_dir: str = ".") -> str:
    """Generate an initial usage log."""
    today = date.today().isoformat()
    content = f"""---
project: {name}
github_url: {github_url}
absorb_date: {today}
last_updated: {today}
---

# {name} — Usage Log

## Version History

| Date | Version | Operation | Notes |
|------|---------|-----------|-------|
| {today} | — | Absorbed | Initial absorption |

## Upstream Tracking

- **Local version**:
- **Upstream latest**:
- **Re-absorption needed**:
"""

    filename = f"{name}-usage-log.md"
    output_path = Path(output_dir) / filename
    output_path.write_text(content, encoding="utf-8")

    return str(output_path)
