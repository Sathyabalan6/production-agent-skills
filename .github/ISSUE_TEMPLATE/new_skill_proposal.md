---
name: New Skill Proposal
about: Propose a new production-grade Agent Skill
title: '[PROPOSAL]: '
labels: enhancement, skill-proposal
assignees: ''
---

**Skill Name:**
Must be lowercase, hyphenated, and $\le 64$ characters (e.g. `api-idempotency-engine`).

**Problem Statement:**
What specific failure modes or vibe-coding degradations do AI agents exhibit without this skill?

**Discriminative Trigger Scope:**
- **Positive Triggers:** When should an agent activate this skill?
- **Negative Exclusions:** What queries should explicitly NOT activate this skill?

**Proposed Progressive Disclosure Structure:**
- Tier 1: Frontmatter metadata
- Tier 2: Core procedural rules & syntactic constraints (<500 lines)
- Tier 3: Supporting references, test scripts, or CI templates

**Deterministic Verification Gate:**
How will the agent or CI verify compliance programmatically (e.g. CLI tool, Playwright test, Semgrep rule)?
