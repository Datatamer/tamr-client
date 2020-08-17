# 2. Linting and formatting

Date: 2019-01-14

## Status

Accepted

## Context

Inconsistent code formatting slows down development and the review process.

Code should be linted for things like:
- unused imports and variables
- consistent import order

Code formatting should be done automatically or programmatically, taking the burden off of reviewers.

## Decision

For linting, use [flake8](https://flake8.pycqa.org/en/latest/) and [flake8-import-order](https://github.com/PyCQA/flake8-import-order).

For formatting, use [black](https://github.com/psf/black).

## Consequences

All linting and formatting are enforced programmatically.

Most linting and formatting errors can be autofixed.

Text editors and IDEs are able to integrate with our linting and formattings tools to automatically fix (most) errors on save.