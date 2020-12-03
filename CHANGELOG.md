## 0.14.0-dev
   **BETA** 
  Important: Do not use BETA features for production workflows.
  - [#438](https://github.com/Datatamer/tamr-client/pull/438) Now able to get, initiate and cancel Tamr backups and restores

## 0.13.0
  **BETA** 
  Important: Do not use BETA features for production workflows.
  - [#383](https://github.com/Datatamer/tamr-client/issues/383) Added function to get operation from resource ID
  - [#421](https://github.com/Datatamer/tamr-client/pull/421) Added functions for getting and replacing the transformations of a projects via `tc.transformations.get_all()` and `tc.transformations.replace_all()`
    - Added new dataclasses `Transformations` and `InputTransformations` to support these functions
  - [#425](https://github.com/Datatamer/tamr-client/pull/425) Now able to get, update and delete manual labels for Categorization projects
  - [#428](https://github.com/Datatamer/tamr-client/pull/428) Moved function `tc.attribute.from_dataset_all` to `tc.dataset.attributes`
  - [#434](https://github.com/Datatamer/tamr-client/pull/434) Added `tc.instance.version` function to get Tamr Version
  - [#435](https://github.com/Datatamer/tamr-client/pull/435) Now able to create projects of the following type in Tamr: Categorization, Mastering, Schema Mapping
  - [#440](https://github.com/Datatamer/tamr-client/pull/440) Added functions for initiating basic mastering workflow operations in `tc.mastering`
  - [#443](https://github.com/Datatamer/tamr-client/pull/443) Added function to materialize datasets.
  - [#445](https://github.com/Datatamer/tamr-client/pull/445) Added functions for getting projects and datasets by name via `tc.project.by_name` and `tc.dataset.by_name`
    - Renamed functions `from_resource_id` to `by_resource_id` in `tc.attribute`, `tc.dataset`, `tc.operation`, and `tc.project`
  - [#446](https://github.com/Datatamer/tamr-client/pull/446) Added functions for categorization workflow operations in `tc.categorization` and schema mapping workflow operations in `tc.schema_mapping`
  - [#452](https://github.com/Datatamer/tamr-client/pull/452) Added functions for creating and deleting a dataset via `tc.dataset.create` and `tc.dataset.delete`
    - Added function for deleting all records in a dataset via `tc.record.delete_all`
    - Added functions for getting all datasets and projects in a Tamr instance via `get_all` functions in `tc.dataset` and `tc.project`
  - [#454](https://github.com/Datatamer/tamr-client/pull/454) Added first `tamr_client` tutorial "Get Tamr version"
  - [#456](https://github.com/Datatamer/tamr-client/pull/456) Added first example `tamr_client` script `examples/get_tamr_version.py`
  - [#461](https://github.com/Datatamer/tamr-client/pull/461) Added functions for golden record workflow operations in `tc.golden_records`
  - [#462](https://github.com/Datatamer/tamr-client/issues/462) Added function for checking operations, raising exception when operation has failed
  - [#469](https://github.com/Datatamer/tamr-client/pull/469) Added "Continuous Mastering" `tamr_client` tutorial
  
  **NEW FEATURES**
  - [#383](https://github.com/Datatamer/tamr-client/issues/383) Now able to create an Operation from Job resource id

  **BREAKING CHANGES**
  - [#468](https://github.com/Datatamer/tamr-client/pull/468) `Dataset.upsert_records` and `Dataset._update_records` no longer take general `**json_args` arguments and will only accept `ignore_nan`
    - The `ignore_nan` argument in `Dataset.upsert_records`, `Dataset._update_records`, `Dataset.upsert_from_dataframe`, and `DatasetCollection.create_from_dataframe` is now deprecated and will be removed in a future release

## 0.12.0
  **BETA**
  Important: Do not use BETA features for production workflows.
  - [#372](https://github.com/Datatamer/tamr-client/issues/372) TC:Design for unified datasets
    - `AnyDataset` can be any type of dataset.
    - Unified Dataset is `tc.dataset.unified.Dataset`
    - Any other Dataset is `tc.dataset.dataset.Dataset`
  - Added function to get unified dataset from its project
  - Added function to commit unified dataset
 
  - [#367](https://github.com/Datatamer/tamr-client/issues/367) Support for projects:
    - generic projects via `tc.project`
    - Mastering projects via `tc.mastering.project`
  - Support for streaming records from a dataset via `tc.record.stream`
  - Support for operations via `tc.operations`
  - `tc.TamrClientException` as a base class for all `tamr_client` exceptions

  **BUG FIXES**
  - `from_geo_features` now returns information on the operation.  
  
  **NEW FEATURES**
  - Added user documentation on [Geospatial functionalities with GeoPandas](https://github.com/Datatamer/tamr-client/blob/master/docs/user-guide/geo.md). Documented limitations in Geopandas and workarounds. 
  - [#366](https://github.com/Datatamer/tamr-client/issues/366) Now able to connect to Tamr instance with implicit port
  - [#376](https://github.com/Datatamer/tamr-client/issues/376) Added user documentation on [Working with Pandas](https://github.com/Datatamer/tamr-client/blob/master/docs/user-guide/pandas.md). 
  
## 0.11.0
  **BETA**

  Important: Do not use BETA features for production workflows.

  New `tamr_client` package includes:

  - attributes
    - `tc.attribute` module
      - `tc.Attribute` type
      - functions: `from_resource_id`, `from_dataset_all`, `to_json`, `create`, `update`, `delete`
    - `tc.attribute_type` module
      - `tc.AttributeType` for type annotations
      - Primitive Types: `BOOLEAN`, `DOUBLE`, `INT`, `LONG`, `STRING`
      - Complex Types: `Array`, `Map`, `Record`
      - functions: `from_json`, `to_json`
    - `tc.subattribute` module
      - `tc.SubAttribute` type
      - functions: `from_json`, `to_json`
    - `tc.attributes.type_alias` module
      - `tc.attributes.type_alias.DEFAULT` type
      - `tc.attributes.type_alias.GEOSPATIAL` type
  - datasets
    - `tc.dataset` module
      - `tc.Dataset` type
      - functions: `from_resource_id`
    - `tc.record` module
      - functions: `tc.record.upsert`, `tc.record.delete`
    - `tc.dataframe` module
      - functions: `tc.dataframe.upsert`
  - `tc.instance` module
    - `tc.Instance` type
    - functions: `tc.instance.from_auth`
  - other supporting modules
    - `tc.auth` module
      - `tc.UsernamePasswordAuth` type
    - `tc.session` module
      - `tc.Session` type
      - functions: `tc.session.from_auth`
    - `tc.url` module
      - `tc.URL` type
    - `tc.response` module
      - functions: `successful`, `ndjson`

  **NEW FEATURES**
  - [#35](https://github.com/Datatamer/tamr-client/issues/35) projects.by_name() functionality added. Can now fetch a project by its name.
  - [#377](https://github.com/Datatamer/tamr-client/issues/377) dataset.upsert_from_dataframe() functionality added. Can now upsert records from a pandas DataFrame.

  **BUG FIXES**
  - Links from our docs to the `requests` docs were outdated. Links have been updated to point to the new `requests` docs URL.
  - [#323](https://github.com/Datatamer/tamr-client/issues/323) Documentation for setting `dtype=str` before calling `client.datasets.create_from_dataframe`

## 0.10.0
  **BREAKING CHANGES**
  - [#309](https://github.com/Datatamer/tamr-client/issues/309) Migrate `SubAttribute` to use `@dataclass(frozen=True)`. `SubAttribute.__init__` constructor replaced with the one generated by `@dataclass`. `SubAttribute`s should be constructed via the `SubAttribute.from_json` static method.
  - [#307](https://github.com/Datatamer/tamr-client/issues/307) Logging improvements: (1) Use standard logging best practices (2) log response body for responses containing HTTP error codes. Previous way to configure logging (via `Client.logger` and `Client.log_entry`) have been replaced. See [User Guide > Logging](https://tamr-client.readthedocs.io/en/latest/user-guide/logging.html).

  **NEW FEATURES**
  - [#295](https://github.com/Datatamer/tamr-client/issues/295) Official support for Python 3.6+. CI now tests against Python 3.6, 3.7, 3.8 .

  **BUG FIXES**
  - [#293](https://github.com/Datatamer/tamr-client/issues/293) Better handling for HTTP 204 on already up-to-date operations

## 0.9.0
  **BREAKING CHANGES**
  - `AttributeMapping.__init__()` now takes arguments `client` and `data` (used to take only `data`).

  **NEW FEATURES**
  - [#218](https://github.com/Datatamer/unify-client-python/issues/218) Delete a `BaseResource`
  - [#233](https://github.com/Datatamer/unify-client-python/issues/233) Remove an input dataset from a project
  - [#67](https://github.com/Datatamer/unify-client-python/issues/67) Create a dataset from a pandas `DataFrame`
  - [#222](https://github.com/Datatamer/unify-client-python/issues/222) Dataset spec to update an existing dataset
  - [#225](https://github.com/Datatamer/unify-client-python/issues/225) Attribute configuration spec to update an existing attribute configuration
  - [#223](https://github.com/Datatamer/unify-client-python/issues/223) Update an attribute with an attribute spec
  - [#224](https://github.com/Datatamer/unify-client-python/issues/224) Project spec to update a project
  - [#275](https://github.com/Datatamer/unify-client-python/issues/275) Create a category with a category spec
  - [#273](https://github.com/Datatamer/unify-client-python/issues/273) Attribute type spec to allow for attribute creation
  - [#219](https://github.com/Datatamer/tamr-client/issues/219) Delete a resource from collection.
  - [#277](https://github.com/Datatamer/unify-client-python/issues/277) Attribute mapping spec
  - [#226](https://github.com/Datatamer/tamr-client/issues/226) Update published cluster configurations with put
  - [#246](https://github.com/Datatamer/tamr-client/issues/246) Cascading dataset delete
  - [#221](https://github.com/Datatamer/unify-client-python/issues/221) delete an attribute mapping

  **BUG FIXES**
  - [#235](https://github.com/Datatamer/unify-client-python/issues/235) Making `AttributeCollection` retrieve attributes directly instead of by streaming
  - [#234](https://github.com/Datatamer/tamr-client/issues/234) Project's `resource`'s `add_input_dataset` now uses params instead of constructing resource ID manually
  - [#256](https://github.com/Datatamer/unify-client-python/issues/256) Record and published clusters refresh did not use the correct endpoint

## 0.8.0
  **BREAKING CHANGES**
  - [#175](https://github.com/Datatamer/unify-client-python/issues/175) `AttributeCollection` no longer has a `from_json` method or a `data` parameter in its constructor
  - `AttributeType` no longer inherits from `BaseResource` (no API path), removing its `from_json` method and `relative_id` property
  - The type of `AttributeType`'s `attributes` property is now a `list` of `SubAttribute`s, which are identical to `Attribute`s except they lack an API path
  - The `Dataset` function `update_records` has been renamed `_update_records` as the convenience functions `upsert_records` and `delete_records` now exist.
  - All files have been refactored:
    * The `models` directory has been deleted, everything previously in it has been moved directly into the base directory
    * `DatasetProfile` and `DatasetStatus` have been moved into the `dataset` directory
    * `machine_learning_model.py` has been renamed `base_model.py`
    * Attribute configurations have been moved to a subdirectory within `project`
    * A `mastering` directory has been created with all mastering specific entities
    * A `categorization` directory has been created with all categorization specific entities, including a `category` subdirectory

  **NEW FEATURES**
  - [#174](https://github.com/Datatamer/unify-client-python/issues/174) Get and create taxonomy categories
  - [#182](https://github.com/Datatamer/unify-client-python/issues/182) Add the ability to refresh estimated pair counts.
  - [#184](https://github.com/Datatamer/unify-client-python/issues/184) Support for getting published cluster configurations
  - [#201](https://github.com/Datatamer/unify-client-python/issues/201) Support for refreshing published cluster IDs
  - [#112](https://github.com/Datatamer/unify-client-python/issues/112) Support for attribute configurations
  - [#181](https://github.com/Datatamer/unify-client-python/issues/181) Support for seeing a dataset's usage
  - [#202](https://github.com/Datatamer/unify-client-python/issues/202) Support for refreshing published cluster stats
  - [#194](https://github.com/Datatamer/unify-client-python/issues/194) Allowing additional JSON parameters to be used for update of records
  - [#205](https://github.com/Datatamer/unify-client-python/issues/205) Update a dataset's records with records rather than record updates
  - [#111](https://github.com/Datatamer/unify-client-python/issues/111) support for schema mapping attributes
  - Delete records from a dataset by providing records rather than record updates
  - [#183](https://github.com/Datatamer/unify-client-python/issues/183) Retrieve versions of published clusters
  - [#220](https://github.com/Datatamer/unify-client-python/issues/220) Delete all records from a dataset
  - [#185](https://github.com/Datatamer/unify-client-python/issues/185) Retrieve versions of published clusters for records
  - [#180](https://github.com/Datatamer/unify-client-python/issues/180) Support for getting a dataset's upstream datasets

  **BUG FIXES**
  - [#212](https://github.com/Datatamer/unify-client-python/issues/212) Sped up slow running tests

## 0.7.0
  **BREAKING CHANGES**
  - [#156](https://github.com/Datatamer/unify-client-python/issues/156) Fetch Dataset profile, even if out of date.
  - [#161](https://github.com/Datatamer/unify-client-python/issues/161) Move `create_attribute` from Dataset to AttributeCollection
  - The `Project` method `add_source_dataset` has been renamed `add_input_dataset` to model the API endpoint.

  **NEW FEATURES**
  - [#65](https://github.com/Datatamer/unify-client-python/issues/65) Fetches published clusters with data represented as a dataset.
  - [#155](https://github.com/Datatamer/unify-client-python/issues/155) Adds read-only support for binning model.
  - [#165](https://github.com/Datatamer/unify-client-python/issues/165) Add `geo_attr` parameter to `Dataset.itergeofeatures()` and `Dataset.from_geo_features()`
  - [#113](https://github.com/Datatamer/unify-client-python/issues/113) Add support for uploading a binningModel
  - [#168](https://github.com/Datatamer/unify-client-python/issues/168) Add support for project attributes
  - [#171](https://github.com/Datatamer/unify-client-python/issues/171) Add support for creating and retrieving taxonomies
  - [#178](https://github.com/Datatamer/unify-client-python/issues/178) Add support for retrieving input datasets

  **BUG FIXES**
  - [#148](https://github.com/Datatamer/unify-client-python/issues/148) Fix null geo, id and absent id bug for geospatial datasets.
  - [#161](https://github.com/Datatamer/unify-client-python/issues/161) DatasetCollection.create() and ProjectCollection.create() don't work
  - [#165](https://github.com/Datatamer/unify-client-python/issues/165) Dataset.itergeofeatures() is too slow

## 0.6.0
  **BREAKING CHANGES**
  - [#150](https://github.com/Datatamer/unify-client-python/issues/150) Move `create_project` and `create_dataset` from client.py to corresponding collection.py

  **NEW FEATURES**
  - [#121](https://github.com/Datatamer/unify-client-python/issues/121) Fetches record clusters with data represented as a dataset.

  **BUG FIXES**
  - [#140](https://github.com/Datatamer/unify-client-python/issues/140) Dataset `itergeofeatures` now supports data with geo attribute NULL
  - [#123](https://github.com/Datatamer/unify-client-python/issues/123) Fix base_path bug for a custom api endpoint

## 0.5.0
  **NEW FEATURES**
  - [#94](https://github.com/Datatamer/unify-client-python/issues/94) Add access to Attributes of a Dataset
  - [#103](https://github.com/Datatamer/unify-client-python/issues/103) Dataset `update_records` now returns the JSON response body for the underlying `POST datasets/{id}:updateRecords` call
  - [#98](https://github.com/Datatamer/unify-client-python/issues/98) Add `__geo_interface__` to Dataset
  - [#100](https://github.com/Datatamer/unify-client-python/issues/100) Add `from_geo_features` to Dataset
  - [#116](https://github.com/Datatamer/unify-client-python/issues/116) Add support for associating a dataset with a project
  - [#109](https://github.com/Datatamer/unify-client-python/issues/109) Add support for profiling datasets
  - [#86](https://github.com/Datatamer/unify-client-python/issues/86) Add support for creating projects
  - [#114](https://github.com/Datatamer/unify-client-python/issues/114) Add support for generating pairs estimate
  - [#106](https://github.com/Datatamer/unify-client-python/issues/106) Add support for initializing a source dataset
  - [#107](https://github.com/Datatamer/unify-client-python/issues/107) Add support for creating a dataset attribute

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
