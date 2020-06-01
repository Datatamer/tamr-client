# Style Guide

### Formatting
Code should generally conform to the [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 
  * [Flake8](https://flake8.pycqa.org/en/latest/) is a linter to help check that code is aligned with these formatting requirements
  * [Black](https://black.readthedocs.io/en/stable/) is a formatter that can be used to automatically reformat code to resolve many (but not all) formatting issues
  * For details on using these tools [see here](run-and-build)

### Structure
* Classes with methods should be avoided in favor of simple [dataclasses](https://docs.python.org/3/library/dataclasses.html) and functions

### Google-style docstrings
All functions and class definitions should use [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) and be annotated with [type hints](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#type-annotations).

### Internal Imports
When importing from within <code>tamr-client</code>:
* Use import statements for modules, classes, and exceptions
* Never import functions directly. Instead import the containing module and use <code>module.function</code>
* Use <code>from foo import bar</code> instead of <code>import foo.bar as bar</code>
