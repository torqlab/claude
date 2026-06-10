/**
 * Validate branch name configuration
 * Enforces semantic branch naming: <type>/<ticket_id>-<description>
 */

export default {
  pattern: /^(feat|fix|chore|docs|test|refactor|perf)\/(\d+)-([a-z0-9\-]+)$|^(main|master|develop)$/,
  errorMsg:
    'Branch name must match pattern: <type>/<ticket_id>-<description>\n' +
    'Types: feat, fix, chore, docs, test, refactor, perf\n' +
    'Examples: feat/1-add-auth, fix/42-resolve-bug',
};
