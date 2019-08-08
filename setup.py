import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyHTC",
    version="0.0.1",
    author="Axel Poyet",
    author_email="axel.poyet@cern.ch",
    description="A python package to ease the job submission to HTCondor, and to organize data. ",
    url="https://github.com/apoyet/pyHT",
    packages=setuptools.find_packages(),
)