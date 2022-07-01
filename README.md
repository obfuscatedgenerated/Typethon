# Typethon

![100% pure](https://img.shields.io/badge/100%25-pure-brightgreen) ![any color, so long as it's black](https://img.shields.io/badge/any%20color%2C%20so%20long%20as%20it's-black-black) ![wheel, yes](https://img.shields.io/pypi/wheel/typethon) [![pypi version](https://img.shields.io/pypi/v/typethon)](https://pypi.org/project/typethon/#history) [![pypi downloads](https://img.shields.io/pypi/dm/typethon)](https://pypi.org/project/typethon/#files)

Typethon is an extremely lightweight and simple module for strongly typed Python.

Typethon has **zero dependencies**, nada, zilch! Typethon *doesn't even use imports from the standard library!* (except for argument parsing in the CLIs, but they are completely optional and only provide linting / building functionality)

(There are dependencies for development and building, but they are not acquired on installing Typethon.)

## Installation from [PyPI](https://pypi.org/project/typethon/)

1. Install via pip: `pip install typethon`

## Decorator Example
    
```python
from typethon.decorators import *

@ReturnType(types=int, constraints=(lambda x: x > 0), use_arg_passing=False) # ReturnType must go before if disabling arg passing, although I have not found a reason for a user to do so
@ArgumentTypes(types={"a": int, "b": int}, constraints={"a": (lambda x: x > 0, lambda x: x < 10), "b": (lambda x: x > 0, lambda x: x < 10)}, use_arg_passing=False)
def constrained_add(a, b):
    return a + b

@ArgumentTypes(use_annotations=True, constraints={"b": (lambda x: x > 0, lambda x: x <= 100)})
@ReturnType(types=type(None)) # must use NoneType to specify we actually want to restrict the return type to None, not just have no restriction
def multiplier_procedure(a: str, b: int):
    print(a * b)

@ReturnType(use_annotations=True)
def silent_procedure() -> None: # the annotation parser handles None to NoneType conversion automagically here
    print("Hello World!")

@Strict() # syntactic sugar for @ArgumentTypes(use_annotations=True) combined with @ReturnType(use_annotations=True), this does not accept any arguments
def strict_uppercase(a:str) -> str:
    print(a)
    return a.upper()

@Strict(arg_constraints={"a": (lambda x: x > 0, lambda x: x < 5)}, return_constraints=(lambda x: x > 0, lambda x: x < 10)) # Strict also accepts constraints, denoted as separate arguments
def strict_constrained_multiply(a:int) -> int:
    print(a)
    return a * 2

print(constrained_add(1,2))
multiplier_procedure("hello", 3)
silent_procedure()
print(strict_uppercase("hi!"))
strict_constrained_multiply(4)
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
