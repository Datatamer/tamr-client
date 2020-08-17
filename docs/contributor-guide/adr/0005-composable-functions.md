# 5. Composable functions

Date: 2019-11-01

## Status

Accepted

## Context

We need a reasonable tradeoff between ease-of-use and maintainability.

Specifically, we need composable, combinable units that can be improved independently.

### Approach 1: Classes + Methods

One approach is to embrace Object-Oriented Programming (OOP) with fluent interfaces (i.e. method chaining):

```python
project
    .create(...)
    .update(...)
    .delete(...)
```

Characteristics:
- Ease-of-use is maximized, but this requires each method to `return self`.
- Also, this approach implies that if a function can be called with X different object types,
each of those object types should have a corresponding method that applies that functionality and then `return self`.

How to enforce these characteristics?

Any solution will be a tax on maintainability, as code that adheres to these characteristics will include many non-semantic lines simply going through the motions of `return self` and copying function usage into dedicated methods for each class.

### Approach 2: Types + Functions

Another approach is to embrace a functional programming style: simple types and functions (no methods).

Usage is not as terse as for OOP:

```python
p = tc.project.create(...)
u = tc.project.update(p, ...)
d = tc.project.delete(p, ...)
```

Characteristics:
- Ease-of-use is not optimized, but still reasonable.
    - With tab-completion, ease-of-use is comparable to OOP.
- Each type can be made immutable
- Each function can be made pure
- Functionality can be shared by calling the same function in user-land, not copying function calls in contributor-land.

## Decision

Use `@dataclass(frozen=True)` to model types and plain Python modules and functions to capture business logic.

## Consequences

Immutable types and pure functions make the code much easier to reason about,
drastically cutting down the time to ramp up and debug.

Functions are easily composable without accumulating undesired side-effects, unlike methods.

Note that not all types and functions *have* to be immutable and pure,
but immutable types and pure functions should be the default.

If there are good reasons to make exceptions, we can do so, but we should include comments to explain why that exception was made.

