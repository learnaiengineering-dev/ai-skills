import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_rules  # noqa: E402
from validate_skills import check_skill, main  # noqa: E402

EXPECTED = {"agent-approval-policy-review", "business-case-builder", "fde-interview-coach"}


def write_skill(tmp_path, folder, text):
    d = tmp_path / folder
    d.mkdir(parents=True)
    f = d / "SKILL.md"
    f.write_text(text)
    return f


def test_repo_skills_are_valid():
    assert main() == 0


def test_expected_skills_exist():
    found = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    assert EXPECTED <= found


def test_readme_lists_every_skill():
    readme = (ROOT / "README.md").read_text()
    for name in EXPECTED:
        assert f"skills/{name}/SKILL.md" in readme


def test_rejects_name_mismatch_and_short_description(tmp_path):
    f = write_skill(tmp_path, "foo", "---\nname: bar\ndescription: short\n---\nbody\n")
    assert len(check_skill(f)) == 2


def test_rejects_non_portable_key(tmp_path):
    desc = "A description that is comfortably longer than forty characters."
    f = write_skill(tmp_path, "foo", f"---\nname: foo\ndescription: {desc}\ncontext: fork\n---\nbody\n")
    assert any("non-portable" in p for p in check_skill(f))


def test_rejects_broken_link(tmp_path):
    desc = "A description that is comfortably longer than forty characters."
    f = write_skill(tmp_path, "foo", f"---\nname: foo\ndescription: {desc}\n---\nSee [x](references/nope.md)\n")
    assert any("broken link" in p for p in check_skill(f))


def test_rejects_missing_frontmatter(tmp_path):
    f = write_skill(tmp_path, "foo", "no frontmatter")
    assert check_skill(f)


def test_generated_dist_is_up_to_date():
    assert build_rules.main(["--check"]) == 0


def test_cursor_rule_is_agent_requested_and_self_contained():
    mdc = (ROOT / "dist" / "cursor-rules" / "business-case-builder.mdc").read_text()
    assert mdc.startswith("---\ndescription: ")
    assert "alwaysApply: false" in mdc
    assert "Reference: assumptions-register.md" in mdc
    assert "(references/" not in mdc


def test_install_script_copies_skill_into_tool_folder(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    env = {"HOME": str(home), "PATH": "/usr/bin:/bin"}
    cmd = [str(ROOT / "scripts" / "install.sh"), "agents", "business-case-builder"]
    subprocess.run(cmd, check=True, env=env, capture_output=True)
    assert (home / ".agents" / "skills" / "business-case-builder" / "SKILL.md").exists()
    assert (home / ".agents" / "skills" / "business-case-builder" / "references").is_dir()


def test_install_script_project_scope_and_dry_run(tmp_path):
    env = {"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"}
    script = str(ROOT / "scripts" / "install.sh")
    subprocess.run([script, "copilot", "--project", "--dry-run"], cwd=tmp_path, check=True, env=env, capture_output=True)
    assert not (tmp_path / ".github").exists()
    subprocess.run([script, "copilot", "--project", "fde-interview-coach"], cwd=tmp_path, check=True, env=env, capture_output=True)
    assert (tmp_path / ".github" / "skills" / "fde-interview-coach" / "SKILL.md").exists()


def test_install_script_rejects_unknown_tool_and_skill(tmp_path):
    env = {"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"}
    script = str(ROOT / "scripts" / "install.sh")
    assert subprocess.run([script, "nope"], env=env, capture_output=True).returncode != 0
    assert subprocess.run([script, "claude", "no-such-skill"], env=env, capture_output=True).returncode != 0
