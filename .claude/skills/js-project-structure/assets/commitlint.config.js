/**
 * Commitlint configuration for conventional commits
 * Extends @commitlint/config-conventional with torq-specific rules
 *
 * Rules:
 * - type-enum: Allowed commit types
 * - scope-empty: Scope is required (never empty)
 * - subject-case: Subject must be lowercase
 * - subject-full-stop: No period at end
 */

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-empty': [2, 'never'],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
  },
};
