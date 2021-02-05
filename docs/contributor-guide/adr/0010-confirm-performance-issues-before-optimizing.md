# 10. Confirm performance issues before optimizing

Date: 2021-02-04

## Status

Accepted

## Context

There are multiple, equally-effective ways to implement many features.  In some cases, the most 
straightforward implementation might involve making more API calls than are strictly necessary 
(e.g. `tc.dataset.create` makes an additional call to retrieve the created dataset from the server
to construct the returned `Dataset`).

## Decision

The simplest and most understandably-written implementation of a feature should be prioritized over
performance or reducing the number of API calls.  When real performance issues are identified, 
optimization should be done on an as-needed basis.

## Consequences

Functions will not be unnecessarily optimized at the cost of readability.