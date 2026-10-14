# Contributing

Thanks for helping! Small, focused PRs are best.

## Adding or changing a skill

1. Create `skills/<name>/SKILL.md` where `<name>` is lowercase kebab-case.
2. Frontmatter: only `name`, `description`, `license` (these work in every supported tool). Put *when to use it* in the `description`; that is what makes tools load the skill at the right time.
3. Keep `SKILL.md` under 500 lines. Move detail to `references/*.md` and link it with a relative path.
4. Do not invent facts or numbers inside a skill. Skills must tell the model to ask, or to label figures as illustrative.
5. Run:

   ```bash
   python scripts/validate_skills.py
   python scripts/build_rules.py      # regenerates dist/
   pip install pytest && pytest -q
   ```

6. Add the skill to the table in `README.md` (a test checks this).
7. Open a PR describing what the skill is for and how you tried it.

Please do not edit files in `dist/` by hand; they are generated.

Be kind. Issues and ideas are welcome.
