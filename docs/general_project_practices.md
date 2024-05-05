# Python

- PEP8.
- OO.
- Use a combination of both Docstrings for every single function and markdown documentation.

## Javascript

- Register events listeners with property style
- Dont use multiline lambda functions, just define them instead. Stick to single line lambda fxs.
- Use parenthesis enclosed lambda function parameters

## SQL

- Use parameterized queries to prevent SQL injection.

## Design

- Always write your tests first. This project used TDD as a requirement. In fact if you commit your tests before writing your code that'd be even better. Then the repository will visually reflect the TDD practice.
- Use fail-fast. Always validate any input as soon as it's recieved, don't trust anything.
- Throw an error/exception if an unexpected state's detected, such as an invalid input. DO NOT guess what somebody might've intended.
- Only open resources just in time to use them, and close them immediately when you're done.
- Always close your own resources, and only close your resources.

- Regularly refactor your code to improve its structure and readability and to reduce complexity.

## Documentation

- All documentation will be formalized and written in GitHub. Some can be left on teams / videos.
- Document names should continue to be in snake case.

## Collaboration

- Assign your self to issues that you're working on.
- Don't complete other's assignment unless deadlines are approach and you give sufficient (quantify this) notice.

- Regular team meetings can help keep everyone on the same page and provide opportunities to discuss any issues or concerns. Unfortunately we cannot get everyone together and some just don't care so this has been a nightmare.

- Regular code reviews can help maintain code quality and consistency. They also provide opportunities for team members to learn from each other. This is dependent on some of our non-existent members actually doing this though.

## Branches

- Name branches descriptively. No generic nondescript "Working Branch".
- Sort common changes to a common branch.

## PRs

- Pull requests are mandatory.
- After PR, branches should be peer reviewed prior to approving merge. This applies to CODE AND DOCUMENTATION PRs.
- Request review with GH Issues, if better comms are required (ping someone, further clarification, etc), Teams will be supplemented.
- Branches for this project will be specific. Once branch is confirmed to be correct and working by Peer Review, the branch can be merged and then deleted.

## Markdown Files

- Markdown files should not have a numbered system for anything that is not to be in consecutive order, such as user stories.
- If a list is in order, use a numbered system.

## Commits

- Write clear and concise commit messages describing the changes you have made.
- Strive to use the present tense ("Add feature" not "Added feature").
- Strive to use the imperative mood ("Move cursor to..." not "Moves cursor to...").

## Reporting Bugs/Requesting Features

- Use the issue tracker on the GitHub repository to report bugs or request new features.
- Please check the existing issues to avoid duplicates.
- Clearly describe the issue or feature, including steps to reproduce the bug if applicable.

## Security Practices

- Regularly review your code for potential security issues. This could include things like checking for SQL injection vulnerabilities, ensuring secure password handling, and regularly updating dependencies.

## Testing

- [automated testing] Implementing unit tests and integration tests can help catch bugs early and ensure that changes don't break existing functionality. We will use `pytest` for Python and maybe `jest` for JavaScript.
- Continuous Integration/Continuous Deployment (CI/CD): Automating the build and deployment process can help catch issues early and streamline deadlines. We can use GitHub Actions for this.
