# absorb-osp WORKFLOW SPECIFICATION v2.0

> The complete specification for systematic open-source project evaluation, absorption,
> internalization, integration, and evolution.

---

## Core Philosophy

### Three Principles

| Principle | Meaning | Check |
|-----------|---------|-------|
| **Scrutinize, Don't Idolize** | Every project is security-audited. Check for malware, vulnerabilities, and safety issues. Reject with clear reasoning. | Security gate at every step |
| **Absorb, Don't Copy** | Not just cloning — understand core capabilities and integrate into your agent ecosystem. Must produce tangible artifacts. | Artifact checklist at step 6 |
| **Evolve, Don't Accumulate** | Merge similar projects, upgrade complementary ones, retire redundant ones. The system must get stronger, not bigger. | Quarterly consolidation at step 12 |

### Five Absorption Depths

| Level | Depth | Artifacts | Use Case |
|-------|-------|-----------|----------|
| L1 | Knowledge | Analysis report + instinct file | Documentation, tutorials, reference |
| L2 | Tool | L1 + invocable skill | CLI tools, script libraries |
| L3 | Service | L2 + startup scripts + proxy route | Web apps, API services |
| L4 | Plugin | L1 + MCP server config | MCP-compatible tools, data sources |
| L5 | Deep | L3 + L4 + code-level integration + workflow orchestration | Core capability additions |

### Integration Targets

| Target | Integration Method | Priority |
|--------|-------------------|----------|
| AI Agent Skills | Skill trigger words + call templates | P0 |
| MCP Server Registry | MCP JSON configuration | P1 |
| HTTP Proxy | Reverse proxy route + health endpoint | P1 |
| Workflow Engine | Workflow node definitions | P2 |
| Monitoring Dashboard | Health check endpoint registration | P2 |

---

## The 12-Step Closed-Loop Flywheel

```
                  ┌─────────────────────────────────────────────┐
                  │              Step 0: Trigger                 │
                  │    GitHub URL / user request / discovery     │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 1: Triage  ⏱ <30s              │
                  │   Quick scan: security redline? eligible?    │
                  │   Output: PASS / FAIL / DEFER                │
                  └──────────────────┬──────────────────────────┘
                                     │ PASS
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 2: Verify                       │
                  │  GitHub metadata, License, recency, malware  │
                  │  Output: verification report, Gate ✅/❌     │
                  └──────────────────┬──────────────────────────┘
                                     │ ✅
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 3: Evaluate                     │
                  │  Tech stack, architecture, API, integration  │
                  │  Security deep scan, dependency risk audit   │
                  │  Output: analysis report                     │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 4: Judge                        │
                  │  5-dimension scoring matrix → depth decision │
                  │  Output: scorecard + L1-L5 decision          │
                  └──────────────────┬──────────────────────────┘
                                     │ Worth absorbing
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 5: Classify                     │
                  │  Compare with existing absorbed projects     │
                  │  Decision: MERGE / SUPERSEDE / ENHANCE /     │
                  │            STANDALONE                        │
                  │  Output: classification + integration plan   │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 6: Internalize                  │
                  │  Create artifacts per L1-L5 depth:           │
                  │  report / skill / MCP / scripts / instincts  │
                  │  Output: artifact files                      │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 7: Load                         │
                  │  Dependency install, build, startup verify   │
                  │  Output: running local service/tool          │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 8: Integrate                    │
                  │  Connect to proxy / MCP / skills / workflow  │
                  │  Output: multi-system call chain working     │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 9: Verify                       │
                  │  Full chain: build + API + integration       │
                  │  + resource + security re-check              │
                  │  Output: verification report, Gate ✅/❌     │
                  └──────────────────┬──────────────────────────┘
                                     │ ✅
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 10: Sync                        │
                  │  Update INDEX.md + absorbed database         │
                  │  + memory system + instincts                 │
                  │  Output: all indexes and memory updated      │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 11: Iterate                     │
                  │  Create usage log, set up upstream tracking  │
                  │  Output: usage_log.md + update plan          │
                  └──────────────────┬──────────────────────────┘
                                     │
                  ┌──────────────────▼──────────────────────────┐
                  │         Step 12: Evolve                      │
                  │  Merge similar projects, upgrade capabilities│
                  │  Improve the workflow itself                 │
                  │  Output: system upgrade + spec iteration     │
                  └─────────────────────────────────────────────┘
```

---

## Detailed Step Specifications

### Step 0: Trigger

**Entry points:**
1. User provides a GitHub URL (auto-trigger)
2. User explicitly requests absorption of a project
3. Auto-discovery (trending repos, user conversation mentions)

**Action:** Validate URL is a valid GitHub repository URL.

---

### Step 1: Triage ⏱ <30 seconds

**Goal:** Quickly determine if the project is worth the full workflow.

| Check | Pass Condition | Reject Condition |
|-------|----------------|------------------|
| Security redline | No malicious code indicators | Cryptominer, backdoor, data exfil, obfuscated scripts |
| Basic eligibility | ≥100 stars OR clear documented purpose | 0 stars, no README, vague description |
| Relevance | Within capability domain of your system | Completely unrelated domain |
| Absorbability | Has a public license | No license, commercial-use prohibited |

**Security Red-Flag Checklist** (any one = FAIL):

- [ ] `eval()` / `exec()` without input sanitization
- [ ] Network requests to hardcoded unknown IPs/domains
- [ ] Install scripts (`install.sh`, `postinstall.js`) with undeclared behavior
- [ ] Binary blobs (`.exe`, `.dll`, `.so`) without corresponding source
- [ ] Code obfuscation (hex encoding, base64 decode-execute patterns)
- [ ] Dependencies containing known malicious packages
- [ ] Unresolved open security issues on the repo

**Decision:**
- **PASS** → Step 2
- **FAIL** → Log reason to `reject_log.md`, explain to user
- **DEFER** → Log to `defer_log.md`, wait for conditions to mature

---

### Step 2: Verify

**Goal:** Deep verification of project trustworthiness.

```yaml
verification:
  github:
    - stars: count and growth trend
    - license: type (MIT/Apache/GPL/Other)
    - last_commit: recent activity date
    - open_issues: count and severity
    - contributors: background of key contributors
  safety:
    - dependabot_alerts: GitHub security alerts
    - code_scanning: CodeQL analysis results
    - secret_scanning: leaked credentials
    - known_vulnerabilities: CVE lookup
  quality:
    - ci_status: CI pipeline passing
    - test_coverage: documented coverage
    - documentation: completeness
    - community: community activity level
```

**Output:** Verification section in analysis report
**Gate:** All three domains green ✅ / any red with clear risk ❌

---

### Step 3: Evaluate

**Goal:** Full understanding of technical architecture and core capabilities.

**Actions:**
1. **Tech stack analysis**: Language, framework, runtime, dependency tree
2. **Architecture analysis**: Directory structure, core modules, data flow, state management
3. **API audit**: HTTP API / CLI / Library API / SDK
4. **Integration point identification**:
   - Can it run as HTTP service? (→ L3/L5)
   - Can it be invoked as CLI? (→ L2)
   - Can it integrate as MCP? (→ L4)
   - Can it be imported as library? (→ L5)
   - Does it provide web UI? (→ L3 accessory)
5. **Security deep scan**:
   - Known vulnerabilities in dependency tree
   - Hardcoded secrets (API keys, tokens, passwords)
   - Insecure default configurations
   - Permission overreach
6. **Dependency evaluation**:
   - Runtime dependency count and size
   - GPU / special hardware requirements
   - External network service requirements
   - Root/admin privilege requirements

**Output:** Full analysis report using `templates/analysis_report.md`

---

### Step 4: Judge — 5-Dimension Scoring Matrix

**Goal:** Quantify the project's value to your system. Decide absorption depth.

| Dimension | Weight | 1pt | 2pt | 3pt | 4pt | 5pt |
|-----------|--------|-----|-----|-----|-----|-----|
| **Capability Fit** | 30% | Completely redundant | Slight overlap | Somewhat complementary | Good complement | Fills a gap |
| **Feasibility** | 25% | Cannot deploy | Difficult | Deployable | Easy to deploy | Zero-config |
| **Interface Compat** | 20% | Cannot integrate | Complex CLI | Has HTTP API | Standard API | MCP native |
| **Maintenance Cost** | 15% | Heavy deps | Above average | Moderate | Lightweight | Zero deps |
| **Security Risk** | 10% | High risk | Elevated | Moderate | Low risk | Zero risk |

**Formula:** `Score = Σ(Dimension × Weight)`

**Decision Threshold:**

| Score | Decision | Depth |
|-------|----------|-------|
| ≥ 4.0 | Strong absorb | L5 Deep Integration |
| 3.0 – 3.9 | Absorb | L3/L4 Service/Plugin |
| 2.0 – 2.9 | Conditional absorb | L1/L2 Knowledge/Tool |
| < 2.0 | Reject | Log to reject_log.md |

---

### Step 5: Classify — Deduplication & Merge Decision

**Goal:** Compare with existing absorbed projects to avoid redundant work.

**Actions:**
1. Search `shared/INDEX.md` for functionally similar projects
2. Search absorbed project analysis reports for capability overlaps
3. Decide based on comparison:

| Decision | Condition | Action |
|----------|-----------|--------|
| **MERGE** | High overlap with existing project | Merge new capabilities into existing artifact |
| **SUPERSEDE** | New project comprehensively beats existing | Mark existing as deprecated, migrate to new |
| **ENHANCE** | New project complements existing gaps | Create bridge that uses both together |
| **STANDALONE** | No overlap — new domain | Independent absorption |

**Output:** Classification decision recorded in analysis report

---

### Step 6: Internalize

**Goal:** Create standardized artifacts matching the chosen absorption depth.

**By depth:**

```
L1 Knowledge:
  ├── analysis_report.md           ← Required
  └── instincts/<name>.md          ← Recommended

L2 Tool (L1 +):
  └── skills/<name>/SKILL.md       ← Required

L3 Service (L2 +):
  ├── start-<name>.sh              ← Startup script (Unix)
  ├── start-<name>.ps1             ← Startup script (Windows)
  └── proxy route config           ← Reverse proxy route

L4 Plugin (L1 +):
  ├── mcp-servers/<name>.json       ← MCP server config
  └── skills/<name>/SKILL.md       ← Companion skill

L5 Deep (L3 + L4 +):
  ├── Code integration               ← Direct import/call
  ├── Multi-skill orchestration      ← Cross-skill call chain
  ├── Workflow integration           ← Workflow nodes
  └── Health check endpoint          ← Monitoring registration
```

**Check:** Every artifact must have complete YAML frontmatter and follow template format.

---

### Step 7: Load

**Goal:** Ensure the project runs in the local environment.

**Checklist:**
- [ ] Dependencies installed without errors
- [ ] Build/compilation successful
- [ ] Service starts and listens on expected port
- [ ] Resource usage acceptable (CPU < 20%, RAM < 500MB)
- [ ] Port does not conflict with existing services
- [ ] Startup script is idempotent (safe to re-run)

---

### Step 8: Integrate

**Goal:** Connect the absorbed project into the agent ecosystem.

**Integration targets (by priority):**

| Target | Method | Priority |
|--------|--------|----------|
| AI Agent Skills | Skill trigger words + call templates | P0 |
| MCP Server Registry | MCP JSON configuration registration | P1 |
| HTTP Proxy | Reverse proxy route + health endpoint | P1 |
| Workflow Engine | Workflow node definitions | P2 |
| Monitoring Dashboard | Health check endpoint registration | P2 |

**Actions:**
1. Create integration code for each target
2. Test the complete call chain
3. Update related skill documentation with integration details

---

### Step 9: Verify

**Goal:** End-to-end confirmation that absorption is complete and working.

```yaml
verification_domains:
  build:
    - Build successful
    - No warnings
  api:
    - Core endpoints return expected results
    - Error handling works correctly
    - Performance is acceptable
  integration:
    - Agent skill triggers work
    - MCP tools registered
    - Proxy routes functional
    - Workflow nodes active
  resource:
    - CPU usage reasonable
    - Memory usage reasonable
    - No port conflicts
    - Disk usage acceptable
  security_recheck:
    - Service listens on localhost only
    - No unauthorized access endpoints
    - No new critical vulnerabilities in dependencies
```

**Gate:** All domains green ✅ / Any red ❌ (fix and re-verify)

---

### Step 10: Sync

**Goal:** Ensure all index and memory systems reflect the new absorption.

**Update locations:**

| Location | Update | Action |
|----------|--------|--------|
| `shared/INDEX.md` | Add project row | Append table row |
| `shared/reject_log.md` or `shared/defer_log.md` | Remove if previously listed | Remove entry |
| Agent memory system | Add permanent memory entry | Write project memory |
| Agent instincts | Add or update relevant instinct | Write/update domain instinct |

---

### Step 11: Iterate

**Goal:** Establish ongoing tracking for the absorbed project.

**Actions:**
1. Create `usage_log.md` documenting first successful call
2. Record current upstream version
3. Create usage baseline (call frequency, success rate)
4. Provide user with usage examples and documentation links

**Usage log tracking:**
- Version history (date, version, operation, notes)
- Call statistics (monthly calls, success rate, avg response time)
- Issue tracking (date, issue, status, resolution)
- Upstream tracking (latest version, update available?, re-absorption needed?)

---

### Step 12: Evolve

**Goal:** Continuous system evolution through consolidation, upgrades, and workflow improvement.

#### A. Quarterly Consolidation
- Scan `shared/INDEX.md` for all absorbed projects
- Group by capability domain
- Evaluate merge candidates within each domain
- Execute merges: keep strongest, retire redundant

#### B. Continuous Upgrades
- After each new absorption: assess which existing projects could benefit
- Create bridge integrations between complementary projects
- Update documentation to reflect current capability landscape

#### C. Workflow Self-Improvement
- Review all absorption cases from the past quarter
- Collect feedback on failed or inefficient steps
- Update this WORKFLOW_SPEC.md
- Bump version number
- Announce workflow update

---

## Security Audit — Cross-Cutting Concern

Each step has a specific security focus:

| Step | Security Focus |
|------|----------------|
| 1 Triage | Malicious code pattern detection |
| 2 Verify | Known vulnerabilities (CVE), dependency safety |
| 3 Evaluate | Hardcoded secrets, permission overreach, network audit |
| 4 Judge | Risk weighting in scoring |
| 5 Classify | Security consistency of merge targets |
| 6 Internalize | Sensitive info in generated artifacts |
| 7 Load | Install script audit, runtime privileges |
| 8 Integrate | API auth, unauthorized access prevention |
| 9 Verify | Security hardening confirmation |
| 10 Sync | Sensitive data protection in memories |
| 11 Iterate | New vulnerability tracking |
| 12 Evolve | Post-merge security consistency |

### Rejection Standards

Reject absorption immediately if any of these are found:

1. **Malicious code**: Cryptominer, backdoor, data exfiltration, ransomware
2. **Critical unpatched vulnerabilities**: RCE, SQL injection, auth bypass
3. **License incompatibility**: GPL/AGPL that cannot be worked around
4. **Hidden behavior**: Install script performs undocumented network/file operations
5. **Supply chain risk**: Dependencies include known compromised packages
6. **Permission overreach**: Requests system privileges beyond functional needs

---

## Template System

All generated artifacts must use the provided templates to ensure consistency.

| Artifact | Template | Purpose |
|----------|----------|---------|
| Analysis report | `templates/analysis_report.md` | Project deep-dive |
| Usage log | `templates/usage_log.md` | Ongoing tracking |
| Instinct | `templates/instinct.md` | Lightweight knowledge |

### Template Usage Rules

1. Copy template to target path during each absorption
2. Fill in according to template format
3. Remove template instructions (comments)
4. Validate: required frontmatter fields present, all sections complete

---

## Quality Metrics

After each absorption, evaluate:

| Metric | Target | How |
|--------|--------|-----|
| Absorption completeness | 100% (all applicable steps done) | Step completion rate |
| Artifact count | ≥ 2 (analysis + at least 1 other) | Artifact count |
| Integration points | ≥ 1 target connected | Integration count |
| Template coverage | All required fields filled | Template fill rate |
| Security score | ≥ 4.0 / 5.0 | Security audit rating |

---

## Workflow Version Management

| Version | Date | Changes |
|---------|------|---------|
| v2.0.0 | 2026-05-23 | 8→12 steps, added Triage/Classify/Sync/Evolve, scoring matrix, depth levels, security gates, template system, quality metrics |
| v1.0.0 | 2026-05-15 | Initial 8-step absorption workflow |

### Iteration Rules

1. Review this specification at least once per quarter
2. Bump version on every change
3. Record all changes in the version table
4. Notify users of major changes

---

> "Scrutinize every project, absorb its essence, internalize its capability, evolve the whole system.
>  No blind trust. No redundant accumulation. No superficial cloning.
>  Every absorbed project must genuinely expand the system's intelligence boundary."
