"""Validate every skills/<name>/SKILL.md so it works in all supported tools.

Rules enforced:
  * YAML frontmatter with `name` (equal to the folder, lowercase kebab-case, max 64 chars)
    and a one-line `description` of 40 to 1024 characters
  * only portable frontmatter keys (tool-specific keys break other tools)
  * a non-empty body, at most 500 lines
  * every relative markdown link points at a file that exists

Exit code is 1 on any problem.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata"}
MAX_BODY_LINES = 500


def parse(text: str):
    """Return (frontmatter dict, body) or (None, text) when there is no frontmatter."""
    m = FM.match(text)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def check_skill(path: Path) -> list[str]:
    problems = []
    fm, body = parse(path.read_text())
    if fm is None:
        return [f"{path}: missing YAML frontmatter"]
    folder = path.parent.name
    name = fm.get("name", "")
    if name != folder:
        problems.append(f"{path}: name {name!r} must equal folder {folder!r}")
    if not NAME.match(name) or len(name) > 64:
        problems.append(f"{path}: name must be lowercase kebab-case, at most 64 chars")
    desc = fm.get("description", "")
    if not 40 <= len(desc) <= 1024:
        problems.append(f"{path}: description must be 40 to 1024 characters (got {len(desc)})")
    if desc in (">", "|", ">-", "|-"):
        problems.append(f"{path}: description must be a single line, not a block scalar")
    extra = set(fm) - PORTABLE_KEYS
    if extra:
        problems.append(f"{path}: non-portable frontmatter keys {sorted(extra)}")
    if not body.strip():
        problems.append(f"{path}: empty body")
    if len(body.splitlines()) > MAX_BODY_LINES:
        problems.append(f"{path}: body over {MAX_BODY_LINES} lines; move detail to references/")
    for target in LINK.findall(body):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        if not (path.parent / target.split("#")[0]).exists():
            problems.append(f"{path}: broken link {target!r}")
    return problems


def main(root: Path = SKILLS) -> int:
    files = sorted(root.glob("*/SKILL.md"))
    problems = [p for f in files for p in check_skill(f)]
    for p in problems:
        print(p)
    print(f"checked {len(files)} skills, {len(problems)} problems")
    return 1 if problems or not files else 0


if __name__ == "__main__":
    sys.exit(main())
