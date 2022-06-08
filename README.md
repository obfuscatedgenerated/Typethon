# Typethon

Typethon is an extremely lightweight and simple module for strongly typed Python.

Typethon has **zero dependencies**, nada, zilch! Typethon *doesn't even use imports from the standard library!* (except for argument parsing in the CLIs, but they are completely optional and only provide linting / building functionality)

(There are dependencies for development and building, but they are not acquired on installing Typethon.)

## Installation

1. Install via pip: `pip install typethon`

## Development

1. Clone the repository: `git clone https://github.com/obfuscatedgenerated/typethon.git`
2. (optional but recommended) Create a virtual environment: `python -m venv env` (or `python3 -m venv env`) and then activate it: `.\env\Scripts\activate` (or `source env/bin/activate`)
3. Install build/dev dependencies: `pip install -r requirements.txt`
4. Once you've made changes, add yourself as a contributor: `python build_tool.py add_contributor <your username>` then commit and make a PR.

- VSCode users: it's recommended to use the Pylance language server as opposed to the Jedi language server as Jedi has issues with wrapper functions when displaying function signatures. You can do this by installing the Pylance extension and changing/setting the `python.languageServer` to `Pylance` in your settings.json file.

# Building

1. Make sure all build/dev dependencies are installed: `pip install -r requirements.txt`
2. From your virtual environment (if you used one, otherwise just run as usual): `python build_tool.py build`

## Featured Tools

...