import os

from setuptools import find_packages, setup

project_root = os.path.dirname(__file__)
with open(os.path.join(project_root, "VERSION.txt"), encoding="utf-8") as f:
    version = f.readline().rstrip()

with open(os.path.join(project_root, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tamr_unify_client",
    version=version,
    description="Python Client for the Tamr Unify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Datatamer/unify-client-python",
    license="Apache 2.0",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["requests>=2.20.0"],
    extras_require={
        "dev": [
            "Sphinx==1.8.2",
            "black==18.9b0",
            "flake8==3.7.7",
            "flake8-import-order==0.18.1",
            "pytest==3.8.2",
            "responses==0.10.4",
            "twine==1.13.0",
            "wheel==0.32.3",
        ]
    },
    maintainer="Pedro Cattori",
    maintainer_email="pedro.cattori@tamr.com",
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
    ],
)
