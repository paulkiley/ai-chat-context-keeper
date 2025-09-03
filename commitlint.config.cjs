module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Allow slightly longer subjects for clarity when needed
    'header-max-length': [2, 'always', 120],
  },
};
