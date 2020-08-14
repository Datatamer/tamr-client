# 8. Standardized imports

Date: 2020-06-01

## Status

Accepted

## Context

Python has many ways of importing:

```python
# option 1: import module

# option 1.a
import foo.bar.bazaar as baz
baz.do_the_thing()

# option 1.b
from foo.bar import bazaar as baz
baz.do_the_thing()

# option 2: import value
from foo.bar.bazaar import do_the_thing
do_the_thing()
```

Not to mention that each of these styles may be done with relative imports (replacing `foo.bar` with `.bar` if the `bar` package is a sibling).

Confusingly, Option 1.a and Option 1.b are _conceptually_ the same, but mechanically there are [subtle differences](https://stackoverflow.com/questions/24807434/imports-in-init-py-and-import-as-statement/24968941#24968941).


## Decision

Imports within `tamr_client`:
- Must import statements for modules, classes, and exceptions
- Must `from foo import bar` instead of `import foo.bar as bar`
- Must not import functions directly. Instead import the containing module and use `module.function(...)`
- Must not use relative imports. Use absolute imports instead.

## Consequences

Standardized import style helps linter correctly order imports.

Choosing import styles is a syntactic choice without semantic meaning.
Removing this choice should speed up development and review.