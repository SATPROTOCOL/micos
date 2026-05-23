<#
.SYNOPSIS
    absorb-osp — Open Source Project Absorption Workflow
    Installer for Windows (PowerShell)

.DESCRIPTION
    Installs the absorb-osp workflow for Claude Code and optionally Hermes Agent.

.PARAMETER Prefix
    Installation directory (default: ~\.claude)

.PARAMETER Hermes
    Also install Hermes Agent configuration

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Prefix "$env:USERPROFILE\.claude"
    .\install.ps1 -Hermes
#>

param(
    [string]$Prefix = "$env:USERPROFILE\.claude",
    [switch]$Hermes
)

$REPO_URL = "https://github.com/SATPROTOCOL/micos"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Info  { Write-Host "[INFO]" -ForegroundColor Blue -NoNewline; Write-Host " $args" }
function Write-Ok    { Write-Host "[OK]"   -ForegroundColor Green -NoNewline; Write-Host "   $args" }
function Write-Warn  { Write-Host "[WARN]" -ForegroundColor Yellow -NoNewline; Write-Host " $args" }
function Write-Error { Write-Host "[ERROR]" -ForegroundColor Red -NoNewline; Write-Host " $args" }

# ── Install for Claude Code ────────────────────────────────────────

function Install-Claude {
    $src = Join-Path $SCRIPT_DIR "claude"
    $dst = $Prefix

    Write-Info "Installing absorb-osp for Claude Code..."
    Write-Info "  Source: $src"
    Write-Info "  Target: $dst"

    # Create directories
    New-Item -ItemType Directory -Force -Path "$dst\skills\absorb-osp" | Out-Null
    New-Item -ItemType Directory -Force -Path "$dst\rules" | Out-Null

    # Copy skill
    $skillSrc = Join-Path $src "SKILL.md"
    if (Test-Path $skillSrc) {
        Copy-Item $skillSrc "$dst\skills\absorb-osp\SKILL.md"
        Write-Ok "Installed skill → $dst\skills\absorb-osp\SKILL.md"
    }

    # Copy workflow spec
    $specSrc = Join-Path $src "WORKFLOW_SPEC.md"
    if (Test-Path $specSrc) {
        Copy-Item $specSrc "$dst\skills\absorb-osp\WORKFLOW_SPEC.md"
        Write-Ok "Installed spec → $dst\skills\absorb-osp\WORKFLOW_SPEC.md"
    }

    # Copy rules
    $rulesSrc = Join-Path $src "rules\absorb-workflow.md"
    if (Test-Path $rulesSrc) {
        Copy-Item $rulesSrc "$dst\rules\absorb-workflow.md"
        Write-Ok "Installed rules → $dst\rules\absorb-workflow.md"
    }

    # Copy templates
    $tmplSrc = Join-Path $SCRIPT_DIR "templates"
    $absorbedDir = "$dst\absorbed"
    New-Item -ItemType Directory -Force -Path $absorbedDir | Out-Null
    if (Test-Path $tmplSrc) {
        Get-ChildItem "$tmplSrc\*.md" | ForEach-Object {
            $destName = "TEMPLATE_$($_.Name)"
            Copy-Item $_.FullName "$absorbedDir\$destName"
            Write-Ok "Installed template → $absorbedDir\$destName"
        }
    }

    # Copy shared indexes (don't overwrite existing)
    $sharedSrc = Join-Path $SCRIPT_DIR "shared"
    if (Test-Path $sharedSrc) {
        Get-ChildItem "$sharedSrc\*.md" | ForEach-Object {
            $destPath = "$absorbedDir\$($_.Name)"
            if (-not (Test-Path $destPath)) {
                Copy-Item $_.FullName $destPath
                Write-Ok "Created index → $destPath"
            } else {
                Write-Warn "Skipping existing: $destPath"
            }
        }
    }
}

# ── Install for Hermes Agent ───────────────────────────────────────

function Install-Hermes {
    $src = Join-Path $SCRIPT_DIR "hermes"
    $hermesConfig = "$env:USERPROFILE\.hermes\config"

    if (-not (Test-Path $hermesConfig)) {
        Write-Warn "Hermes config directory not found at $hermesConfig"
        New-Item -ItemType Directory -Force -Path $hermesConfig | Out-Null
        Write-Info "Created Hermes config directory"
    }

    $yamlSrc = Join-Path $src "absorb-osp.yaml"
    if (Test-Path $yamlSrc) {
        Copy-Item $yamlSrc "$hermesConfig\absorb-osp.yaml"
        Write-Ok "Installed Hermes config → $hermesConfig\absorb-osp.yaml"
    }

    $readmeSrc = Join-Path $src "README.md"
    if (Test-Path $readmeSrc) {
        Copy-Item $readmeSrc "$hermesConfig\absorb-osp-hermes.md"
        Write-Ok "Installed Hermes readme → $hermesConfig\absorb-osp-hermes.md"
    }
}

# ── Main ───────────────────────────────────────────────────────────

Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     absorb-osp  Installation             ║" -ForegroundColor Cyan
Write-Host "║     v2.0.0                               ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Install-Claude

if ($Hermes) {
    Install-Hermes
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Installation Complete!                   ║" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "║  Next steps:                              ║" -ForegroundColor Cyan
Write-Host "║  1. Restart your agent session            ║" -ForegroundColor Cyan
Write-Host "║  2. Send a GitHub URL to test:            ║" -ForegroundColor Cyan
Write-Host '║     "Absorb https://github.com/..."       ║' -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "║  Docs: $REPO_URL           ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
