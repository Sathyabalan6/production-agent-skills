# Contributing to Production Agent Skills

Thank you for your interest in contributing to the **Production Agent Skills** suite! We welcome community contributions that expand, harden, and optimize skills for autonomous AI coding agents.

---

## The Agent Skills Open Standard

Every skill in this repository strictly adheres to the open standard originally introduced by Anthropic in late 2025 and adopted across frameworks like Cursor, Codex, and Google Antigravity.

### Structural Requirements

A skill must be contained in its own directory with lowercase alphanumeric characters and single non-consecutive hyphens:

```text
skills/my-new-skill/
├── SKILL.md            # Mandatory: Core procedural logic & YAML frontmatter (<500 lines)
├── scripts/            # Optional: Executable test suites, linters, or calculation utilities
├── assets/             # Optional: CI workflows, boilerplate configurations, or schemas
└── references/         # Optional: Deep architectural manuals, proofs, and extended checklists
```

### Three-Tier Progressive Disclosure

1. **Tier 1: Discovery (Frontmatter Metadata)**
   - Pre-loaded by the host agent at session boot.
   - `name`: Must be $\le 64$ characters and match the folder name exactly.
   - `description`: Must be $\le 1024$ characters. Must include explicit positive activation triggers and explicit negative exclusions.
   - `compatibility`: Runtime dependencies (Node, Python, Playwright, Semgrep).
   - **Token Budget**: $\sim 100$ tokens per skill.

2. **Tier 2: Activation (`SKILL.md`)**
   - Loaded into context only when triggered.
   - **Line Budget**: Strictly **$< 500$ lines** ($< 5,000$ tokens) to preserve the model's active reasoning capacity.
   - **Instructional Stance**: Prescriptive operational directives and strict syntactic constraints (no vague narrative suggestions).
   - **Plan-Validate-Patch**: The instructions must direct the agent to inspect the codebase, validate against test boundaries, and emit surgical diffs.

3. **Tier 3: Deep Execution (`references/`, `scripts/`, `assets/`)**
   - Ingested on-demand when specialized sub-tasks arise.

---

## Local Development & Validation

Before submitting a Pull Request, run the automated test suite locally:

```bash
# Validate all skills against standard constraints
python3 scripts/validate-skills.py

# Test the installer in dry-run mode
bash install.sh --dry-run
```

All skills must pass with zero errors before being merged.

---

## Submitting a Pull Request

1. Fork the repository and create a feature branch (`git checkout -b skill/my-new-skill`).
2. Implement your skill following the directory structure and progressive disclosure tiers.
3. Add an entry to the table in `README.md`.
4. Ensure `python3 scripts/validate-skills.py` passes cleanly.
5. Submit a Pull Request targeting the `main` branch.
