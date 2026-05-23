---
name: absorb-osp
preamble-tier: 1
version: 2.0.0
description: |
  Systematic open-source project absorption closed-loop flywheel — security triage →
  deep evaluation → quantified judging → dedup classification → multi-depth
  internalization → load → integrate → verify → sync → iterate → evolve (12 steps).
  Triggers automatically on GitHub URLs.
triggers:
  - absorb open source
  - analyze open source project
  - open source project
  - evaluate this project
  - integrate
  - absorb
  - open source
  - github.com
  - load project
  - internalize
  - absorb-osp
  - assess project
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch
  - AskUserQuestion
  - Agent
  - Glob
  - Grep
  - Skill
---

# absorb-osp v2.0.0 — Open Source Project Absorption Workflow

## Workflow Specification

The complete workflow definition, scoring matrix, template system, and security audit
specification are in:

**`WORKFLOW_SPEC.md`** (same directory)

**Always read the full spec before executing.** The 12-step process is mandatory.

---

## 12-Step Closed-Loop Flywheel

```
Trigger(0) → Triage(1) → Verify(2) → Evaluate(3) → Judge(4) → Classify(5)
→ Internalize(6) → Load(7) → Integrate(8) → Verify(9) → Sync(10) → Iterate(11) → Evolve(12)
```

| Step | Name | Core Action |
|------|------|-------------|
| 0 | Trigger | GitHub URL / user request / auto-discovery |
| 1 | Triage | <30s quick scan: security red flags, basic eligibility |
| 2 | Verify | GitHub metadata, license, recency, malware check |
| 3 | Evaluate | Full architecture analysis, API audit, security deep scan |
| 4 | Judge | 5-dimension scoring matrix, decide L1-L5 absorption depth |
| 5 | Classify | Compare with existing absorbed projects, decide MERGE/SUPERSEDE/ENHANCE/STANDALONE |
| 6 | Internalize | Create artifacts: analysis report, skill, MCP config, scripts |
| 7 | Load | Install deps, build, verify startup |
| 8 | Integrate | Connect to proxy, agent skills, MCP, workflow engine |
| 9 | Verify | End-to-end tests: build, API, integration, resource, security |
| 10 | Sync | Update all index files and memory systems |
| 11 | Iterate | Usage log, upstream tracking, issue recording |
| 12 | Evolve | Merge similar projects, upgrade capabilities, self-improve workflow |

---

## Pre-Execution Checklist

Before starting, confirm:

1. **Read WORKFLOW_SPEC.md?** — If not, read it first
2. **Is a GitHub URL provided?** — If not, ask the user
3. **Checked existing absorbed projects?** — Avoid duplicates (see `shared/INDEX.md`)
4. **Templates available?** — Located in `templates/` directory

---

## Quick Reference

### Five Absorption Depths

| Level | Type | When |
|-------|------|------|
| L1 | Knowledge | Pure documentation or reference projects |
| L2 | Tool | CLI tools, script libraries |
| L3 | Service | Web apps, API servers |
| L4 | Plugin | MCP-compatible tools |
| L5 | Deep Integration | Core capability additions (memory, trading, AI) |

### Rejection Criteria (any one triggers rejection)

1. Malicious code (cryptominer, backdoor, data exfiltration)
2. Critical unpatched vulnerabilities
3. Incompatible license (GPL/AGPL where unavoidable)
4. Hidden installer behavior (undeclared network calls, file ops)
5. Supply chain risk (known malicious dependencies)
6. Excessive permissions (beyond functional requirements)

### Required Artifacts (by depth)

```
templates/analysis_report.md     ← Required (all levels)
templates/usage_log.md            ← Step 11
shared/INDEX.md row               ← Step 10
shared/reject_log.md               ← If rejected (Step 1)
shared/defer_log.md                ← If deferred (Step 1)
claude/skills/<name>/SKILL.md      ← L2+
claude/mcp-servers/<name>.json     ← L4
claude/instincts/<name>.md         ← L1+
```

---

## References

- [WORKFLOW_SPEC.md](./WORKFLOW_SPEC.md) — Full specification
- [rules/absorb-workflow.md](./rules/absorb-workflow.md) — Enforcement rules
- [shared/INDEX.md](../shared/INDEX.md) — Absorbed projects index
