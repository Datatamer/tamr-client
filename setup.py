from setuptools import find_packages, setup
import os

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
    keywords=["tamr", "unify"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
