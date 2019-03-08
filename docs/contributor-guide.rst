Contributor Guide
=================

Code of Conduct
---------------

See `CODE_OF_CONDUCT.md <https://github.com/Datatamer/unify-client-python/blob/master/CODE_OF_CONDUCT.md>`_

.. _bug-reports-feature-requests:

🐛 Bug Reports / 🙋 Feature Requests
------------------------------------

Please leave bug reports and feature requests as `Github issues <https://github.com/Datatamer/unify-client-python/issues/new/choose>`_ .

----

Be sure to check through existing issues (open and closed) to confirm that the
bug hasn’t been reported before.

Duplicate bug reports are a huge drain on the time of other contributors, and
should be avoided as much as possible.

↪️ Pull Requests
----------------

For larger, new features:

  `Open an RFC issue <https://github.com/Datatamer/unify-client-python/issues/new/choose>`_ .
  Discuss the feature with project maintainers to be sure that your change fits with the project
  vision and that you won't be wasting effort going in the wrong direction.

  Once you get the green light 🚦 from maintainers, you can proceed with the PR.

Contributions / PRs should follow the
`Forking Workflow <https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow>`_ :

  1. Fork it: https://github.com/[your-github-username]/unify-client-python/fork
  2. Create your feature branch::

      git checkout -b my-new-feature

  3. Commit your changes::

      git commit -am 'Add some feature'

  4. Push to the branch::

      git push origin my-new-feature

  5. Create a new Pull Request

----

We optimize for PR readability, so please squash commits before and during the PR
review process if you think it will help reviewers and onlookers navigate your changes.

Don't be afraid to ``push -f`` on your PRs when it helps our eyes read your code.

Installation
------------

  1. Clone your fork and ``cd`` into the project::

      git clone https://github.com/<your-github-username>/unify-client-python
      cd unify-client-python

  2. Create a virtualenv::

      python3 -m venv .venv
      source .venv/bin/activate

    .. note::
      See `User Guide > Installation <user-guide/installation.html>`_ for compatible
      Python versions.

    .. caution::
      If you place your virtualenv within the project codebase, you must name it
      ``.venv`` for ``flake8`` to know how to exclude it from linting.

  3. Install dev dependencies::

      pip install -e .[dev]

Tests
-----

To run all tests::

    pytest .

To run specific tests, see `these pytest docs <https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`_ .

Editor config
-------------

`Atom <https://atom.io/>`_ :

- `python-black <https://atom.io/packages/python-black>`_
- `linter-flake8 <https://atom.io/packages/linter-flake8>`_ (be sure to activate your virtualenv BEFORE opening Atom)
