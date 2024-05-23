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
