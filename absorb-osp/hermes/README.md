# absorb-osp — Hermes Agent Integration

## Overview

This directory contains configuration for integrating the absorb-osp workflow with [Hermes Agent](https://github.com/HermesAgent).

## Installation

### Option 1: Copy to Hermes config directory

```bash
cp -r hermes/* ~/.hermes/config/
```

### Option 2: Symlink

```bash
ln -s $(pwd)/hermes/absorb-osp.yaml ~/.hermes/config/absorb-osp.yaml
```

## What Gets Installed

| File | Purpose |
|------|---------|
| `absorb-osp.yaml` | Hermes MCP tool definitions + proxy routes + system prompt injection |

## MCP Tools Available

After installation, Hermes provides these tools:

| Tool | Description |
|------|-------------|
| `absorb_osp_absorb` | Absorb a project from a GitHub URL |
| `absorb_osp_list` | List all absorbed projects |
| `absorb_osp_status` | Check status of a specific absorbed project |
| `absorb_osp_consolidate` | Run quarterly consolidation workflow |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ABSORBED_UPSTREAM` | `http://localhost:8080` | Upstream URL for absorbed proxy services |

## Usage

Once installed, Hermes will automatically route GitHub URL mentions through the absorb-osp workflow. You can also call the MCP tools directly:

```
User: "Absorb https://github.com/example/awesome-project"
Agent: [triggers absorb_osp_absorb tool → runs 12-step workflow]
```
