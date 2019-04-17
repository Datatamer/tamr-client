# Release process for `tamr-unify-client`

During the following steps, we'll consider releasing the `0.3.0` version as an example.

For our example, that means `master` branch is currently on version `0.3.0-dev` (you can check the actual version in `VERSION.txt`).

Be sure to substitute `0.3.0` appropriately with the actual version being released.

NOTE: You should make sure the commit you plan to use for the release branch is passing CI tests.

# 1. Version bump on `master`

Create a PR with the following changes:
- `Version.txt`: bump the version to the next one, keeping the `-dev` suffix e.g. `0.3.0-dev` -> `0.4.0-dev`.
- `CHANGELOG.md`:
  - Create a new section for the new development version e.g. Add `# 0.4.0-dev` to the top of the changelog (with an empty line between it and the next version header).
  - Remove the `-dev` suffix from the version being released e.g. `# 0.3.0-dev` -> `# 0.3.0`.

Ensure CI tests pass for your PR and merge your changes into `master`.

# 2. Cut a release branch

On the [Datatamer/unify-client-python](https://github.com/Datatamer/unify-client-python) Github repo, click on [Commits](https://github.com/Datatamer/unify-client-python/commits/master). Navigate to the commit just before the version bump commit from Step 1. Click the `<>` icon to browse the repo at that commit.

Then, create a branch on Github within the [Datatamer/unify-client-python](https://github.com/Datatamer/unify-client-python) repo titled `release-<version>` e.g. `release-0.3.0`.

NOTE: This release branch should *not* contain the version bump changes from Step 1.

# 3. Remove `-dev` suffix on release branch

Create a PR *to the release branch* with the following changes:
- `VERSION.txt`: Remove `-dev` suffix from version e.g. `0.3.0-dev` -> `0.3.0`.
- `CHANGELOG.md`: Remove the `-dev` suffix from the version being released e.g. `# 0.3.0-dev` -> `# 0.3.0`.

Ensure CI tests pass for your PR and merge your changes into the release branch e.g. `release-0.3.0`.

# 4. Create a Github release

On the [Datatamer/unify-client-python](https://github.com/Datatamer/unify-client-python) Github repo, click on [Releases](https://github.com/Datatamer/unify-client-python/releases). Click "Draft a new release".

Title the release with the release version. Do not include anything else in the release title e.g.
- Correct: `0.3.0`
- Incorrect: `v0.3.0`
- Incorrect: `Release 0.3.0`

Select the corresponding release branch in the `Target` branch dropdown.

Copy/paste the `CHANGELOG.md` entries for this release into the description for the release (only the entries, not the header since the version number is already encoded as the title for this release).

Create the release. This should also implicitly create a tag for the release under [Tags](https://github.com/Datatamer/unify-client-python/tags).

# 5. Check on published artifacts

We use Travis CI as our Continuous Integration (CI) solution.

CI is wired to ["deploy"](https://github.com/Datatamer/unify-client-python/blob/master/.travis.yml#L14) (a.k.a. publish) releases to PyPI for any tags that look like a semantic version number e.g. `0.3.0`. So CI should handle publishing for you.

Check that CI tests passed.
Check that CI successfully published the release version to [PyPI](https://pypi.org/project/tamr-unify-client/#history).

---

If everything went correctly `pip install -U tamr-unify-client` should install the new release of the Python Client.

If testing/publishing failed on the release branch, make additional PRs to fix any issues and get CI tests to pass. Be sure to merge those fixes into `master` too!
