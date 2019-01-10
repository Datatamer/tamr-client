from setuptools import find_packages, setup

setup(
    name="tamr_unify_client",
    version="0.1.0",
    description="Python Client for the Tamr Unify API",
    url="https://github.com/Datatamer/unify-python-client",
    maintainer="Pedro Cattori",
    maintainer_email="pedro.cattori@tamr.com",
    packages=find_packages(),
    install_requires=["requests==2.19.1"],
)
