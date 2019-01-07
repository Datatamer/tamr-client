## Manual integration testing

Make sure you have a minimal categorization or mastering project running (local or remote is ok).
Ask pedro.cattori@tamr.com for Unify backups that you can restore minimal projects from.

---

Run:

```sh
UNIFY_HOST=10.10.0.61 UNIFY_USERNAME=username UNIFY_PASSWORD=password g :pubapi:client:v1:pyTestFilepath -Pfilepath=python/test/integration
```

replacing `10.10.0.61` with your Unify host, and `username` and `password` with your credentials.

---

You can pass a more specific filepath to run a subset of tests e.g.
```sh
UNIFY_HOST=10.10.0.61 g :pubapi:client:v1:pyTestFilepath -Pfilepath=python/test/integration/test_continuous_mastering.py
```

Running integration tests will produce `.ndjson` files in `test/response_logs`
for use in the Mock API tests.
