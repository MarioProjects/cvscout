from setuptools import setup, find_packages

with open("DESCRIPTION.md", "r") as f:
    description = f.read()

setup(
    name="cvscout",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "openai==1.30.1",
        "langchain==0.2.0",
        "pydantic==2.7.1",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
