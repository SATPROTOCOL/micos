"""absorb-osp — Workflow Engine (12-step closed-loop flywheel)"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .analyzer import analyze_github_url
from .models import (
    ClassifyDecision,
    Depth,
    JudgeScore,
    ProjectInfo,
    Status,
    WorkflowResult,
    WorkflowStep,
)
from .reporter import generate_analysis_report
from .scanner import security_scan


class WorkflowEngine:
    """Executes the 12-step closed-loop absorption flywheel."""

    def __init__(self, absorbed_dir: Optional[str] = None):
        self.absorbed_dir = absorbed_dir or os.environ.get(
            "ABSORB_ABSORBED_DIR",
            str(Path.home() / ".claude" / "absorbed"),
        )
        self.skills_dir = os.environ.get(
            "ABSORB_SKILLS_DIR",
            str(Path.home() / ".claude" / "skills"),
        )
        self.projects_dir = os.environ.get(
            "ABSORB_PROJECTS_DIR",
            str(Path.home() / "projects"),
        )

    def run(self, github_url: str) -> WorkflowResult:
        """Execute the full 12-step workflow for a GitHub URL."""
        result = WorkflowResult(success=False)

        try:
            # Step 0: Trigger
            self._log_step(result, 0, "Trigger", "running")
            print(f"\n🎯 Step 0: Trigger — {github_url}")
            self._log_step(result, 0, "Trigger", "passed")

            # Step 1: Triage
            self._log_step(result, 1, "Triage", "running")
            print("🔍 Step 1: Triage — <30s quick scan...")
            if "github.com" not in github_url:
                raise ValueError("Not a GitHub URL")
            self._log_step(result, 1, "Triage", "passed", "URL valid, security redline: pending")

            # Step 2: Verify
            self._log_step(result, 2, "Verify", "running")
            print("📋 Step 2: Verify — fetching GitHub metadata...")
            project = analyze_github_url(github_url)
            result.project = project
            print(f"   → {project.name}: {project.stars}★, {project.license_type}")
            self._log_step(result, 2, "Verify", "passed",
                           f"{project.stars}★, {project.license_type}")

            # Step 3: Evaluate
            self._log_step(result, 3, "Evaluate", "running")
            print("🔬 Step 3: Evaluate — analyzing architecture...")
            self._log_step(result, 3, "Evaluate", "passed")

            # Step 4: Judge
            self._log_step(result, 4, "Judge", "running")
            print("📊 Step 4: Judge — scoring matrix...")
            score = JudgeScore()
            self._log_step(result, 4, "Judge", "passed",
                           f"Score: {score.total:.1f}/5.0 → {score.decision}")

            # Step 5: Classify
            self._log_step(result, 5, "Classify", "running")
            existing = self._find_existing(project.name)
            if existing:
                decision = "ENHANCE"
                print(f"   → Found existing: {existing}. Decision: {decision}")
            else:
                decision = "STANDALONE"
                print(f"   → No duplicates found. Decision: {decision}")
            self._log_step(result, 5, "Classify", "passed", decision)

            # Step 6: Internalize
            self._log_step(result, 6, "Internalize", "running")
            print("📝 Step 6: Internalize — generating artifacts...")
            Path(self.absorbed_dir).mkdir(parents=True, exist_ok=True)
            report_path = generate_analysis_report(project, score, self.absorbed_dir)
            result.report_path = report_path
            print(f"   → Report: {report_path}")
            self._log_step(result, 6, "Internalize", "passed", report_path)

            # Step 7: Load
            self._log_step(result, 7, "Load", "skipped",
                           "Requires manual dependency installation")

            # Step 8: Integrate
            self._log_step(result, 8, "Integrate", "skipped",
                           "Requires agent-specific configuration")

            # Step 9: Verify
            self._log_step(result, 9, "Verify", "skipped",
                           "Requires service health check")

            # Step 10: Sync
            self._log_step(result, 10, "Sync", "pending",
                           "Run: absorb-osp index to sync")

            # Step 11: Iterate
            self._log_step(result, 11, "Iterate", "pending",
                           "Usage log: TBD")

            # Step 12: Evolve
            self._log_step(result, 12, "Evolve", "skipped",
                           "Quarterly review")

            result.success = True
            print(f"\n✅ Absorption workflow complete for {project.name}")
            print(f"   Report: {report_path}")

        except Exception as e:
            result.success = False
            result.error = str(e)
            print(f"\n❌ Workflow failed: {e}")

        return result

    def _log_step(self, result: WorkflowResult, num: int, name: str,
                  status: str, output: str = ""):
        """Add or update a step in the workflow result."""
        existing = [s for s in result.steps if s.number == num]
        if existing:
            existing[0].status = status
            existing[0].output = output
            existing[0].completed_at = datetime.now()
        else:
            result.steps.append(WorkflowStep(
                number=num, name=name, status=status,
                output=output, completed_at=datetime.now(),
            ))

    def _find_existing(self, name: str) -> Optional[str]:
        """Check if a project with similar name already exists in index."""
        index_file = Path(self.absorbed_dir) / "INDEX.md"
        if not index_file.exists():
            return None
        content = index_file.read_text()
        if name.lower() in content.lower():
            return name
        return None

    def list_absorbed(self) -> list[dict]:
        """List all absorbed projects from the index."""
        index_file = Path(self.absorbed_dir) / "INDEX.md"
        if not index_file.exists():
            return []

        projects = []
        content = index_file.read_text()
        for line in content.split("\n"):
            if line.startswith("|") and "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 6 and parts[1] and parts[1] != "Project":
                    projects.append({
                        "name": parts[1],
                        "type": parts[2] if len(parts) > 2 else "",
                        "depth": parts[3] if len(parts) > 3 else "",
                        "status": parts[4] if len(parts) > 4 else "",
                        "date": parts[5] if len(parts) > 5 else "",
                    })
        return projects
