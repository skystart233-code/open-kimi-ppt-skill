# Contributing

Thank you for improving PPTD Studio Skill.

## Before opening a change

1. Open an issue for behavior changes that affect the PPTD format, exported
   PPTX structure, or compatibility with existing projects.
2. Keep generated presentations and large media out of the package unless they
   are small, necessary test fixtures.
3. Preserve upstream copyright and license headers in vendored files.
4. Record a source URL, pinned revision, license, and local modifications when
   adding or updating vendored software.

## Development checks

Requires Node.js 18+ and Python 3.

```bash
npm test
python -m unittest discover -s skills/pptd-studio/tests -p "test_*.py" -v
npm run pack:check
```

Changes to rendering or export should also be checked with a real multi-page
PPTD project. Verify both the rendered overview and the resulting PPTX ZIP.

## Pull requests

- Explain the problem and the chosen solution.
- Include tests for observable behavior, not wording alone.
- Update README, CHANGELOG, NOTICE, and third-party license files when relevant.
- By submitting a contribution, you agree that it is licensed under the
  repository's MIT License and that you have the right to submit it.
