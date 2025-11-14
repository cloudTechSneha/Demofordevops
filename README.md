# maven-ci-demo

This repository contains a demo Maven project with GitHub Actions to:
- Run `mvn clean verify` (tests + JaCoCo)
- Enforce Spotless formatting and Checkstyle
- Validate PR description contains a JIRA ID
- Validate labels are present on PR
- Post test summary as a PR comment
- Auto-resolve or reopen PR review threads based on test outcome

## How to use
1. Push this project to GitHub.
2. Create a repository secret `GITHUB_TOKEN` (GitHub provides a default token in Actions).
3. Enable branch protection rules on `main` requiring status checks and "Require all conversations to be resolved".
4. Open a PR — workflows will run automatically.

