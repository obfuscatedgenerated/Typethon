# Typethon

Typethon is an extremely lightweight and simple module for strongly typed Python.

Typethon has **zero dependencies**, nada, zilch! Typethon *doesn't even use imports from the standard library!* (except for argument parsing in the CLIs, but they are completely optional and only provide linting / building functionality)

(There are dependencies for development and building, but they are not acquired on installing Typethon.)

## Installation

1. Install via pip: `pip install typethon`

## Decorator Example
    
```python
from typethon.decorators import *

@ReturnType(types=int, constraints=(lambda x: x > 0), use_arg_passing=False) # ReturnType must go before if disabling arg passing, although I have not found a reason for a user to do so
@ArgumentTypes(types={"a": int, "b": int}, constraints={"a": (lambda x: x > 0, lambda x: x < 10), "b": (lambda x: x > 0, lambda x: x < 10)}, use_arg_passing=False)
def my_epic_function(a, b):
    return a + b

@ArgumentTypes(use_annotations=True)
@ReturnType(types=type(None)) # must use NoneType to specify we actually want to restrict the return type to None, not just have no restriction
def funky_function(a: str, b: int):
    print(a * b)

@ArgumentTypes(use_annotations=True)
@ReturnType(use_annotations=True)
def ok_this_is_a_function() -> None:
    print("ok")

print(my_epic_function(1,2))
funky_function("hello", 3)
ok_this_is_a_function()
```

## Development

1. Clone the repository: `git clone https://github.com/obfuscatedgenerated/Typethon.git`
2. (optional but recommended) Create a virtual environment: `python -m venv env` (or `python3 -m venv env`) and then activate it: `.\env\Scripts\activate` (or `source env/bin/activate`)
3. Install build/dev dependencies: `pip install -r requirements.txt`
4. Once you've made changes, add yourself as a contributor: `python build_tool.py add_contributor <your username>` then commit and make a PR.

- VSCode users: it's recommended to use the Pylance language server as opposed to the Jedi language server as Jedi has issues with wrapper functions when displaying function signatures. You can do this by installing the Pylance extension and changing/setting the `python.languageServer` to `Pylance` in your settings.json file.

# Building

1. Make sure all build/dev dependencies are installed: `pip install -r requirements.txt`
2. From your virtual environment (if you used one, otherwise just run as usual): `python build_tool.py build`
