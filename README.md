# ai-skills

Free, practical **AI engineering skills** that work in **Claude Code, Codex, Cursor and GitHub Copilot** (and any tool that reads `SKILL.md` or `AGENTS.md`).

A skill is a folder with a `SKILL.md`: instructions your AI tool loads automatically when your request matches the skill's description. Write it once, use it in every tool.

## Skills

| Skill | Use it when |
|---|---|
| [`agent-approval-policy-review`](skills/agent-approval-policy-review/SKILL.md) | You are deciding which tool calls an AI agent may run alone and which need a human. Produces a tiered policy, findings and tests. |
| [`business-case-builder`](skills/business-case-builder/SKILL.md) | You need to get an AI project funded. Produces options, an assumptions register, best/base/worst cases, risks and a benefits plan, and never invents numbers. |
| [`fde-interview-coach`](skills/fde-interview-coach/SKILL.md) | You are preparing for a Forward Deployed Engineer interview. Runs timed drills, client role-plays and deployment-design rounds, and scores you against a rubric. |

## Install

Pick your tool. Skills are plain folders, so installing is copying a folder.

| Tool | Easiest install | Skills folder it reads |
|---|---|---|
| **Claude Code** | `/plugin marketplace add learnaiengineering-dev/ai-skills` then `/plugin install ai-skills@learnaiengineering` | `.claude/skills/` or `~/.claude/skills/` |
| **Codex** | `scripts/install.sh agents` | `.agents/skills/` or `~/.agents/skills/` |
| **Cursor** | `scripts/install.sh agents` (or `cursor`) | `.agents/skills/`, `.cursor/skills/`, and it also reads `.claude/skills/` |
| **GitHub Copilot** | `scripts/install.sh copilot --project` | `.github/skills/`, `.claude/skills/` or `.agents/skills/`; personal: `~/.copilot/skills/` |
| **Anything else** | Copy [`dist/AGENTS.md`](dist/AGENTS.md) into your tool's instructions file | |

```bash
git clone https://github.com/learnaiengineering-dev/ai-skills.git
cd ai-skills
scripts/install.sh agents                 # all skills, for your user, shared folder
scripts/install.sh claude --project       # all skills, into the current repo for Claude Code
scripts/install.sh copilot business-case-builder   # one skill
scripts/install.sh agents --dry-run       # show what would be copied
```

Cursor rules (for older setups that only read `.cursor/rules`): copy a file from [`dist/cursor-rules/`](dist/cursor-rules/) into `.cursor/rules/`. They are agent-requested, so they load only when relevant.

Folder locations come from each tool's own documentation and can change. If a skill does not appear, check your tool's current docs.

## Try it

After installing, ask your tool in plain language:

- *"Review the approval policy for my agent. Its tools are: send_email, read_crm, create_ticket, issue_refund."*
- *"Help me build a business case for automating invoice matching with AI."*
- *"Run a 25-minute FDE decomposition drill for a healthcare company."*

## Design rules

- **Portable on purpose.** Only `name`, `description` and `license` in the frontmatter, so every tool accepts them.
- **Honest.** Skills tell the model to ask for missing facts and to label placeholder figures as illustrative. They never invent numbers.
- **Small.** Each `SKILL.md` stays under 500 lines; detail lives in `references/`.

## Develop

```bash
python scripts/validate_skills.py      # checks every skill, exits non-zero on problems
python scripts/build_rules.py          # regenerates dist/ (Cursor rules, AGENTS.md)
pip install pytest && pytest -q
```

CI fails if a skill is invalid or if `dist/` is out of date. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Related

- [claude-skills-starter](https://github.com/learnaiengineering-dev/claude-skills-starter): more skills for prompt review, RAG debugging, eval design and agent specs.
- [AI Business Case Builder](https://learnaiengineering.dev/business-case): the free calculator behind the numbers in `business-case-builder`.

---

## Part of Learn AI Engineering

This repo is a free resource from [Learn AI Engineering](https://learnaiengineering.dev/?utm_source=github&utm_medium=repo&utm_campaign=ai-skills) — *Build production AI systems.*

- Structured learning paths, labs and portfolio projects: [https://learnaiengineering.dev](https://learnaiengineering.dev/?utm_source=github&utm_medium=repo&utm_campaign=ai-skills)
- More free repos: [github.com/learnaiengineering-dev](https://github.com/learnaiengineering-dev)

Licensed under MIT.
