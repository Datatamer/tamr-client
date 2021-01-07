# Contributing pull requests

### ️RFCs
If the proposed changes require design input, [open a Request For Comment issue](https://github.com/Datatamer/tamr-client/issues/new/choose).

Discuss the feature with project maintainers to be sure that your change fits with the project vision and that you won't be wasting effort going in the wrong direction.

Once you get the green light 🟢 from maintainers, you can proceed with the PR.

### Pull requests

Contributions / PRs should follow the
[Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow). In short:

  1. Fork it: `https://github.com/[your-github-username]/tamr-client/fork`
  2. Create your feature branch:

      ```sh
      git checkout -b my-new-feature
      ```

  3. Commit your changes:

      ```sh
      git commit -am 'Add some feature'
      ```

  4. Push to the branch:

      ```sh
      git push origin my-new-feature
      ```

  5. Create a new Pull Request

### Commits

Split and squash commits as necessary to create a clean `git` history. Once you ask for review, only add new commits (do not change existing commits) for reviewer convenience. You may change commits in your PR only if reviewers are ok with it.

Commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
CI for pull requests will enforce this and fail if commit messages are not formatted correctly.

We recommend the [Commitzen CLI](https://github.com/commitizen/cz-cli) to make writing Conventional Commits easy, but you may write commit messages manually or use any other tools.

Also, your commit messages should [explain any things that are not obvious](https://chris.beams.io/posts/git-commit/#why-not-how) from reading your code!

### CI checks

Continuous integration (CI) checks are run automatically for all pull requests.
CI runs the same [dev tasks](dev-tasks) that you can run locally.

You should run dev tasks locally _before_ submitting your PR to cut down on subsequent commits to fix the CI checks.
