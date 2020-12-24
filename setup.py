import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmgshell",
    version="0.0.1",
    author="Jean-Pierre Forcioli",
    author_email="jpforcioli@fortinet.com",
    description="A FortiManager shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpforcioli/fmgshell",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)