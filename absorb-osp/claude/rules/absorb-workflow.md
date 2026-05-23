# absorb-osp — Enforcement Rules

> Permanent enforcement rules loaded every session.
> Defines the standard process for all open-source project absorption.

## Core Principles (Priority: High to Low)

1. **Scrutinize, Don't Idolize** — Every project must be security-audited. Reject malicious code with clear reasoning.
2. **Absorb, Don't Copy** — Every project must produce tangible artifacts (skill/MCP/instinct), or absorption is incomplete.
3. **Evolve, Don't Accumulate** — Similar projects must be merged/upgraded. No redundant capabilities allowed.

## Mandatory Execution Steps

Whenever a GitHub URL is received or a user requests project absorption:

### Step 1: Read WORKFLOW_SPEC.md
- Location: `claude/WORKFLOW_SPEC.md` in the absorb-osp project
- Confirm understanding of the full 12-step closed-loop flywheel

### Step 2: Security Redline Check (cannot skip)
- Check for malicious code: cryptominer, backdoor, data exfiltration, obfuscated scripts
- Check license compatibility
- Check known vulnerabilities and dependency risk
- Redline found → Immediately reject and explain why to the user

### Step 3: Deduplication Check (cannot skip)
- Search `shared/INDEX.md` for similar existing projects
- If found → Execute classification step (MERGE/SUPERSEDE/ENHANCE/STANDALONE)

### Step 4: Standardized Output
- Use `templates/analysis_report.md` for the analysis report
- Create artifacts matching the L1-L5 depth standard
- Every artifact must have complete YAML frontmatter

### Step 5: Full-Chain Verification
- Build test passes
- API endpoints respond correctly
- Integration points connected
- Resource usage acceptable
- Security re-check passes

### Step 6: Sync All Indexes
- Update `shared/INDEX.md`
- Update agent memory system
- Create project memory entry

### Step 7: First-Call Usage Log
- Create `usage_log.md`
- Record first successful call

## Rejection Standards

Reject absorption if any:

1. **Malicious code** — Cryptominer, backdoor, ransomware, data exfiltration
2. **Critical unpatched vulns** — RCE, SQL injection, auth bypass
3. **License conflict** — GPL/AGPL that cannot be worked around
4. **Hidden behavior** — Install script performs undeclared actions
5. **Supply chain risk** — Dependencies contain known malicious packages
6. **Permission overreach** — Requests privileges beyond functional need

## Iteration Rules

- Review workflow effectiveness quarterly
- Self-evaluate process efficiency after each absorption
- Collect improvement points and update WORKFLOW_SPEC.md
- Bump version on changes

## Related Files

- Workflow spec: `claude/WORKFLOW_SPEC.md`
- Executable skill: `claude/SKILL.md`
- Project index: `shared/INDEX.md`
- Analysis template: `templates/analysis_report.md`
