# 6. Type-checking

Date: 2020-01-29

## Status

Accepted

## Context

Static type-checking is available for Python, making us of the type annotations already in the codebase.

## Decision

Type-check via [mypy](http://mypy-lang.org/).

## Consequences

Testing is still important, but type checking helps to eliminate bugs via static checking,
even for parts of the code not exercised during tests.

Additionally, type-checking relies on our type annotations, ensuring that the annotations are correct and complete.
