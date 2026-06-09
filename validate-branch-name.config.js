module.exports = {
  pattern: "^(feat|fix|chore|docs|test|refactor|perf)/\\d+-.+$",
  errorMsg:
    "Branch name must follow pattern: <type>/<ticket_id>-<description>\n\nExamples:\n  feat/123-add-feature\n  fix/42-resolve-bug\n  chore/99-update-deps\n\nAllowed types: feat, fix, chore, docs, test, refactor, perf\nTicket ID must be numeric (required).\n\nSee: .claude/skills/semantic-release/SKILL.md for details",
};
