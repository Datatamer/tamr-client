# 9. Separate types and functions

Date: 2020-06-29

## Status

Accepted

## Context

Code must be organized to be compatible with:
- Static type-checking via [mypy](https://github.com/python/mypy)
- Runtime execution during normal usage and running tests via [pytest](https://docs.pytest.org/en/stable/)
- Static doc generation via [sphinx-autodoc-typehints](https://github.com/agronholm/sphinx-autodoc-typehints)

Additionally:
- Functions should be able to refer to any type
- Most types depend on other types non-recursively, but some types (e.g. `SubAttribute` and `AttributeType`) do depend on each other recursively / cyclically.

## Decision

Put types (`@dataclass(frozen=True)`) into the `_types` module
and have all function modules depend on the `_types` module to define their inputs and outputs.

## Consequences

Separating types into a `_types` module (e.g. `tc.Project` is an alias for `tc._types.project.Project`)
and functions into namespaced modules (e.g. `tc.project` is a module containing project-specific utilities)
allows all of our tooling to run successfully.

Also, splitting up types and functions means that we can author a function like `tc.dataset.attributes` in the `tc.dataset` module
while still having the `tc.attribute` module depend on `tc.Dataset` type.

Finally, for the rare cases where cyclical dependencies for types are unavoidable,
we can use [typing.TYPE_CHECKING](https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING) since `mypy` and Python are smart enough to resolve these cyclical correctly via [forward references](https://www.python.org/dev/peps/pep-0484/#forward-references).

