# 4. Documentation and docstrings

Date: 2019-10-03

## Status

Accepted

## Context

Documentation can take four forms:
1. Explanation
2. Tutorial
3. How-to
4. Reference

We need a way to author and host prosey documentation and generate reference docs based on source code.

## Decision

Doc compilation will be done via [sphinx](https://www.sphinx-doc.org/en/master/).

Prosey documentation (1-3) via [recommonmark](https://github.com/readthedocs/recommonmark).

Reference documentation (4) will be generated based on type annotations and docstrings via:
- Automatic docs based on docstrings via [sphinx-autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html), [sphinx-autodoc-typehints](https://github.com/agronholm/sphinx-autodoc-typehints)
- Google-style docstrings via [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- Hosting on [ReadTheDocs](https://readthedocs.org/) (RTD)
- Build docs in CI and fail on errors or warnings.

## Consequences

Prosey documentation can be written in Markdown (.md), which is more familiar to our contributors than .rst format.

Reference doc generation makes docs more maintainable and consistent with actual code.

Google-style docstrings are easier to read than sphinx-style docstrings.

RTD natively compiles documentation using sphinx and simultaneously hosts docs at each version.