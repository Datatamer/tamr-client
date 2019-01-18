# Release process for `tamr-unify-client`

1. Cut a release branch
2. Bump version in [VERSION.txt](VERSION.txt) and add "release candidate" suffix (i.e. `<version>-rc0`)
    If you need to make any fixes during subsequent steps:
    i. Cut a new release branch from the existing release branch
    ii. Make your changes
    iii. Bump the `-rc` version (e.g. `-rc0` -> `-rc1`)
    iv. Continue to Step 3
3. Run CI tests on release branch
4. Update [CHANGELOG](CHANGLOG.md) with new entry containing:
    - Release version
    - Date of release
    - `ADDED` (only if applicable)
    - `REMOVED` (only if applicable)
    - `FIXED` (only if applicable)
5. Build release candidate artifacts
  `python setup.py sdist bdist_wheel`
6. Test publish to test.pypi.org
  `twine upload --repository-url https://test.pypi.org/legacy/ dist/*<rc version>*`
7. Remove `-rc` suffix from version in [VERSION.txt](VERSION.txt)
8. Merge release branch onto `master`
9. Tag latest commit with version number on Github
  `git tag -a v<version> -m "Release v<version>"`
  `git push Datatamer --tags`
10. Build release artifacts
  `python setup.py sdist bdist_wheel`
11. Publish to PyPI
  `twine upload dist/*<version>*`
    - If necessary, update the version/date of the corresponding entry in [CHANGELOG](CHANGELOG.md)
