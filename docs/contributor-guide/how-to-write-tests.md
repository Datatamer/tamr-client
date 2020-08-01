# How to write tests

Our test suite uses `pytest`.

See the [pytest docs](https://docs.pytest.org/en/stable/) for:
- how to run specific tests
- how to capture `print` output for debugging tests
- etc...

Note that you will need to pass any `pytest` arguments after `--` so that `nox` passes the arguments correctly to `pytest`:

```sh
prn -s test-3.6 -- -s tests/tamr_client/test_project.py::test_from_resource_id_mastering
```

## Unit tests

Each unit test:
- must be in a Python file whose name starts with `test_`
- must be a function whose name starts with `test_`
- should test *one* specific feature.
- should use `tests.tamr_client.fake` utility to fake resources and Tamr server responses as necessary

For example, testing a simple feature that does not require communication with a Tamr server could look like:

```python
# test_my_feature.py
import tamr_client as tc
from tests.tamr_client import fake

def test_my_feature_works():
    # prerequisites
    p = fake.project()
    d = fake.dataset()

    # test my feature
    result = tc.my_feature(p, d)
    assert result.is_correct()
```

After using the `fake` utilities to set up your prerequisites,
the rest of the test code should be as representative of real user code as possible.

Test code that exercises the feature should not contain any test-specific logic.

### Faking responses

If the tested feature requires communication with a Tamr server,
you will need to fake Tamr server responses.

In general, any feature that takes a session argument will need faked responses.

You can fake responses via the `@fake.json` decorator:

```python
# test_my_feature.py
import tamr_client as tc
from tests.tamr_client import fake

@fake.json
def test_my_feature():
    # prerequisites
    s = fake.session()
    p = fake.project()

    # test my feature
    result = tc.my_feature(s, p)
    assert result.is_correct()
```

`@fake.json` will look for a corresponding fake JSON file within `tests/tamr_client/fake_json`,
specifically `tests/tamr_client/fake_json/<name of test file>/<name of test function>`.

In the example, that would be `tests/tamr_client/fake_json/test_my_feature/test_my_feature_works.json`.

The fake JSON file should be formatted as a list of request/response pairs in order of execution.

For a real examples, see existing fake JSON files within `tests/tamr_client/fake_json`.