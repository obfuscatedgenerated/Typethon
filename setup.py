import os
from setuptools import setup
import runpy


def read(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    r = f.read()
    f.close()
    return r

with open("requirements.txt", encoding="utf-8") as f:
    all_reqs = f.read().split('\n')


setup(
    name="typethon",
    version=runpy.run_path("./typethon/__version__.py")["__version__"],
    packages=["typethon", "typethon.utils"],
    license="MIT",
    description="Typethon is an extremely lightweight and simple module for strongly typed Python.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="obfuscatedgenerated",
    author_email="pip@obfuscatedgenerated.ml",
    url="https://github.com/obfuscatedgenerated/typethon",
    repository="https://github.com/obfuscatedgenerated/typethon",
    keywords=["type", "check", "decorators", "cli", "lint", "lightweight"],
    install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-')) and ("black" not in x) and ("wheel" not in x)],
    dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' in x],
    entry_points=read("entry_points.toml"),
    package_data={
        "typethon": ["*.json"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
