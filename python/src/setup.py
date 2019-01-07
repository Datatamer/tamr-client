from setuptools import find_packages, setup
import json
import os

# note: gradle needs to be able to *read* values like `name`, `version`,
#       `install_requires`, etc...from a *static, non-executable* file
# read src/main/python/pyproject.json
root = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(root, "pyproject.json")) as f:
    pyproject = json.load(f)

setup(
    name=pyproject["name"],
    version=pyproject["version"],
    description="Python Client for the Tamr Unify API",
    url="https://github.com/Datatamer/javasrc/tree/develop/pubapi/client",
    maintainer="Pedro Cattori",
    maintainer_email="pedro.cattori@tamr.com",
    packages=find_packages(),
    install_requires=pyproject["requires"],
)
