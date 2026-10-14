"""Generate fallback formats for tools that do not read SKILL.md natively.

  dist/cursor-rules/<skill>.mdc   Cursor project rules (agent-requested, never always-on)
  dist/AGENTS.md                  one file for tools that read AGENTS.md (Codex, Windsurf, Aider, ...)

Tools that read SKILL.md (Claude Code, Codex, Cursor, Copilot) should use skills/ directly.

Usage:
  python scripts/build_rules.py          write dist/
  python scripts/build_rules.py --check  exit 1 if dist/ is out of date
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import ROOT, SKILLS, parse  # noqa: E402

DIST = ROOT / "dist"
LINK = re.compile(r"\[([^\]]*)\]\((references/[^)\s]+)\)")


def inline_references(skill_dir: Path, body: str) -> str:
    """Append referenced files to the body so a single generated file is self-contained."""
    refs = []
    for _, rel in LINK.findall(body):
        if rel not in refs:
            refs.append(rel)
    body = LINK.sub(lambda m: f"{m.group(1)} (see Reference: {Path(m.group(2)).name} below)", body)
    parts = [body.rstrip()]
    for rel in refs:
        text = (skill_dir / rel).read_text().strip()
        parts.append(f"\n\n---\n\n## Reference: {Path(rel).name}\n\n{text}")
    return "".join(parts) + "\n"


def demote(text: str, by: int) -> str:
    """Push markdown headings down `by` levels, leaving fenced code alone."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("#"):
            line = "#" * by + line
        out.append(line)
    return "\n".join(out) + "\n"


def build() -> dict[Path, str]:
    files: dict[Path, str] = {}
    agents = [
        "# AI skills from Learn AI Engineering\n",
        "Each section below is a self-contained skill. Apply a section when the user's request "
        "matches its `Use when` line.\n",
    ]
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        fm, body = parse(skill_md.read_text())
        name, desc = fm["name"], fm["description"]
        full = inline_references(skill_md.parent, body)
        files[DIST / "cursor-rules" / f"{name}.mdc"] = (
            f"---\ndescription: {desc}\nalwaysApply: false\n---\n{full}"
        )
        agents.append(f"\n## Skill: {name}\n\n**Use when:** {desc}\n\n{demote(full, 2)}")
    files[DIST / "AGENTS.md"] = "".join(agents)
    return files


def main(argv: list[str]) -> int:
    files = build()
    if "--check" in argv:
        stale = [p for p, c in files.items() if not p.exists() or p.read_text() != c]
        known = set(files)
        stale += [p for p in DIST.rglob("*") if p.is_file() and p not in known]
        for p in stale:
            print(f"out of date: {p.relative_to(ROOT)}")
        return 1 if stale else 0
    for p, c in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(c)
        print("wrote", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
