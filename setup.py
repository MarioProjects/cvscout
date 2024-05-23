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
