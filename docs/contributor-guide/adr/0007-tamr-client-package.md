# 7. tamr_client package

Date: 2020-04-03

## Status

Accepted

## Context

We have an existing userbase that relies on `tamr_unify_client` and cannot painlessly make backwards-incompatible changes.

But, we want to rearchitect this codebase as a [library of composable functions](/contributor-guide/adr/0005-composable-functions).

## Decision

Implement rearchitected design as a new package named `tamr_client`.

Require the `TAMR_CLIENT_BETA=1` feature flag for `tamr_client` package usage.

Warn users who attempt to use `tamr_client` package to opt-in if they want to beta test the new design.

## Consequences

Continue to support `tamr_unify_client`, but any new functionality:
- must be included in `tamr_client`
- may be included in `tamr_unify_client`

Users are required to explicitly opt-in to new features,
preserving backward compatiblitiy for current users.

Once we reach feature parity with `tamr_unify_client`,
we can undergo a deprecation cycle and subsequently remove `tamr_unify_client.
