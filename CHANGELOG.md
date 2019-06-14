## 0.5.0-dev
  **NEW FEATURES**
  - [#94](https://github.com/Datatamer/unify-client-python/issues/94) Add access to Attributes of a Dataset
  - [#103](https://github.com/Datatamer/unify-client-python/issues/103) Dataset `update_records` now returns the JSON response body for the underlying `POST datasets/{id}:updateRecords` call
  - [#98](https://github.com/Datatamer/unify-client-python/issues/98) Add `__geo_interface__` to Dataset
  - [#100](https://github.com/Datatamer/unify-client-python/issues/100) Add `from_geo_features` to Dataset
  - [#109](https://github.com/Datatamer/unify-client-python/issues/109) Add support for profiling datasets
  - [#86](https://github.com/Datatamer/unify-client-python/issues/86) Add support for creating projects
  - [#114](https://github.com/Datatamer/unify-client-python/issues/114) Add support for generating pairs estimate
  - [#106](https://github.com/Datatamer/unify-client-python/issues/106) Add support for initializing a source dataset
  - [#121](https://github.com/Datatamer/unify-client-python/issues/121) Fetches record clusters with data represented as a dataset.
  - [#116](https://github.com/Datatamer/unify-client-python/issues/116) Add support for associating a dataset with a project
  
  **BUG FIXES**
  - [#118](https://github.com/Datatamer/unify-client-python/issues/118) Fix JSON sent for Dataset.update_records

## 0.4.0
  **BREAKING CHANGES**
  - [#61](https://github.com/Datatamer/unify-client-python/issues/61) `data` field renamed to `_data` (private).
  - [#78](https://github.com/Datatamer/unify-client-python/issues/78) Property accessors return `None` rather than raise `KeyError`

  **NEW FEATURES**
  - Record Clusters API endpoint to finish working mastering workflow.
  - [#78](https://github.com/Datatamer/unify-client-python/issues/78) Improved repr for objects through the library
  - [#42](https://github.com/Datatamer/unify-client-python/issues/42) Optional `session` argument to `Client` to use a specific `requests.Session` instance

  **BUG FIXES**
  - Mastering workflow example was missing the generate clusters step, which has been rectified using proper endpoint
  - [#30](https://github.com/Datatamer/unify-client-python/issues/30) Better docs for how to call directly call APIs
  - [#61](https://github.com/Datatamer/unify-client-python/issues/61) `data` field renamed to `_data` (private).

## 0.3.0
*released on 2019-3-1*

  **NEW FEATURES**
  - Versioning example in FAQ
  - Offline installation docs
  - `by_external_id` methods for `Dataset` and `Project`
  - `DatasetStatus` resource (subresource of `Dataset`)
  - `Client.request` accepts absolute paths as relative to origin

  **BUG FIXES**
  - `requests` version specified changed to `>=2.20.0` for Airflow compatibility
  - `setup.py` reads `VERSION.txt` and `README.md` with explicit `utf-8` encodings

## 0.2.0
*released on 2019-1-17*

  **NEW FEATURES**
  - [Docs via readthedocs](https://tamr-unify-python-client.readthedocs.io/en/stable/)
  - [CI testing via TravisCI](https://travis-ci.org/Datatamer/unify-client-python) ([details](https://github.com/Datatamer/unify-client-python/commit/ae381ce29593a70ed992f88a3e3ef3eb170a5cd4))
  - Release process documented in [RELEASE.md](https://github.com/Datatamer/unify-client-python/blob/master/RELEASE.md) ([details](https://github.com/Datatamer/unify-client-python/commit/fe717bbddca96b82bc1e447a93ae5c8817481675))
  - README Badges
    - Version, Python version, License, Codestyle ([details](https://github.com/Datatamer/unify-client-python/pull/1))
    - Docs ([details](https://github.com/Datatamer/unify-client-python/pull/14))
    - CI build/test ([details](https://github.com/Datatamer/unify-client-python/pull/19))
  - HTTP errors raised as exceptions. More helpful than always getting `JSONDecodeError`s. ([details](https://github.com/Datatamer/unify-client-python/pull/7))
  - Stream records from a dataset ([details](https://github.com/Datatamer/unify-client-python/pull/13))
  - Migrate all Python Client docs from docs.tamr.com to Sphinx docs ([details](https://github.com/Datatamer/unify-client-python/pull/21))

  **BUG FIXES**
  - PyPI metadata
    - `-` not `_` in project name ([details](https://github.com/Datatamer/unify-client-python/commit/5e25c45ec9bff0d0f9f40f52e81aacecdccb3e1b))
    - correct github repo URL ([details](https://github.com/Datatamer/unify-client-python/commit/767cf537f247d20293aa3a81b7830534aa6f84ec))
    - "Apache 2.0" as license value ([details](https://github.com/Datatamer/unify-client-python/pull/2))
    - README now parsed/rendered as Markdown ([details](https://github.com/Datatamer/unify-client-python/pull/4))
  - Change Log for 0.1.0 release ([details](https://github.com/Datatamer/unify-client-python/commit/852d6f0fd11f8ea33d2ea49d60a406f4e7267143))
  - readthedocs compatibility ([details](https://github.com/Datatamer/unify-client-python/pull/12))

## 0.1.0
*released on 2019-1-10*

  Initial public release

  **BREAKING CHANGES**
  - Protobuf-related dependencies ([details](https://github.com/pcattori/unify-client-python/commit/5f25bcf41ba64fce67c2cfc1bba81d382bc70efe))

  **NEW FEATURES**
  - Repo Documentation ([details](https://github.com/pcattori/unify-client-python/commit/5f25bcf41ba64fce67c2cfc1bba81d382bc70efe))
    - [CHANGELOG.md](https://github.com/Datatamer/unify-client-python/blob/master/CHANGELOG.md)
    - [CODE_OF_CONDUCT.md](https://github.com/Datatamer/unify-client-python/blob/master/CODE_OF_CONDUCT.md)
    - [LICENSE](https://github.com/Datatamer/unify-client-python/blob/master/LICENSE)
    - [README.md](https://github.com/Datatamer/unify-client-python/blob/master/README.md)
  - Version in [VERSION.txt](VERSION.txt) ([details](https://github.com/pcattori/unify-client-python/commit/41e93d4dba03bc7445f1935345bfd76cf45b877c))

  **BUG FIXES**
  - Reference documentation
    - Autodoc should show inherited members ([details](https://github.com/pcattori/unify-client-python/commit/8356eb3d8ea995227e808a07d71de1bf3d7453c7))
    - Autodoc warning about `**` in `param` docstrings ([details](https://github.com/pcattori/unify-client-python/commit/2a204b294a41e4b9eea5cc383569f6303d3a5206))
    - Shortened Sphinx references with `~` ([details](https://github.com/pcattori/unify-client-python/commit/9827e98dd7dab4eaeaef5e60197e280649de3737))