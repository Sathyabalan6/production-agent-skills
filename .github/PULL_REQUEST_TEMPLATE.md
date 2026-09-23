## Description
Briefly describe the purpose of this PR (new skill, bug fix, or hardening update).

## Agent Skills Conformance Checklist
- [ ] Skill directory matches the `name` field in YAML frontmatter exactly.
- [ ] Frontmatter `name` is lowercase, hyphenated, and $\le 64$ characters.
- [ ] Frontmatter `description` is $\le 1024$ characters and includes explicit positive triggers and negative exclusions.
- [ ] Core `SKILL.md` is strictly under **500 lines** to preserve agent reasoning context.
- [ ] Heavy documentation or extended checklists are placed in `references/`.
- [ ] Executable tests or helper scripts are placed in `scripts/`.
- [ ] Ran `python3 scripts/validate-skills.py` locally and all checks passed (100%).
