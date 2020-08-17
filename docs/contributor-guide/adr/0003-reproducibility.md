# 3. Reproducibility

Date: 2019-06-05

## Status

Accepted

## Context

Reproducing results from a program is challenging when operating systems, language versions, and dependency versions can vary.

For this codebase, we will focus on consistent Python versions and dependency versions.

## Decision

Manage multiple Python versions via [pyenv](https://github.com/pyenv/pyenv).

Manage dependencies via [poetry](https://python-poetry.org/).

Define tests via [nox](https://nox.thea.codes/en/stable/).

Run tests in automation/CI via [Github Actions](https://github.com/features/actions).

## Consequences

This solution lets us:
- keep track of [abstract *and* concrete versions](https://caremad.io/posts/2013/07/setup-vs-requirement/) for dependencies (think `.lock` file)
- locally test against multiple Python versions
- run the same tests locally as we do in [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) (CI)
- easily view CI test results within the review context
