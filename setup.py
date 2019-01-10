from setuptools import find_packages, setup
import os

# path to VERSION.txt
project_root = os.path.dirname(__file__)
with open(os.path.join(project_root, "VERSION.txt")) as f:
    version = f.readline().rstrip()

with open(os.path.join(project_root, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="tamr_unify_client",
    version=version,
    description="Python Client for the Tamr Unify API",
    long_description=long_description,
    url="https://github.com/Datatamer/unify-python-client",
    maintainer="Pedro Cattori",
    maintainer_email="pedro.cattori@tamr.com",
    packages=find_packages(),
    install_requires=["requests==2.19.1"],
)
