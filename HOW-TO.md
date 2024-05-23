# CVScout - How To

## Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
pip install -r dev-requirements.txt
```

## Creating a package

- [Tutorial](https://www.youtube.com/watch?v=Kz6IlDCyOUY)

```bash
pip install setuptools wheel twine
```

Create your code under the package folder (cvscout) and export the functions you want to use in the `__init__.py` file.

Next we need to create a `setup.py` file to define the package and its dependencies.

```python
from setuptools import setup, find_packages

setup(
    name="cvscout",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "langchain",
        "pydantic",
    ],
)
```

This commmand will generate two distributions for us:

```bash
python setup.py sdist bdist_wheel
```

A source distribution, which is usually just the python scripts,
and the wheel distribution, which usually also contains binaries,
which are platform specific. This archives will have all the necessary
files for installing and running the package.

## Local Testing

Before uploading the package to PyPi, we probably will want to test that it works locally.
With the previous command we generated the wheel distribution, which we can install with pip.
This will be placed under the `dist` folder and will have a `.whl` extension.

For example:
```bash
pip install dist/cvscout-0.1-py3-none-any.whl
```

Now we can create a new python script and import the package to test it.

## Publishing the package to PyPi

The first we will need is to create an account in PyPi. Next we can run this command:

```bash
twine upload dist/*
```

This will asks for credentials which we can enter into the terminal directly or provide them as an environment variable, for example for automation of CI/CD pipelines.

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxx
```

Done!

### Using the README.md as the package description

If we access to the published package in PyPi, we will see that the description is empty.
Let's fix that by using the README.md file as the package description.

Go to the `setup.py` file and modify it:

```python
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="cvscout",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "openai==1.30.1",
        "langchain==0.2.0",
        "pydantic==2.7.1",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
```

Now we can update the package in PyPi:

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

Done!