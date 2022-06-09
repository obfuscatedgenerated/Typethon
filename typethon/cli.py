try:
    from typethon.utils.cli_arg_validators import *
except ModuleNotFoundError:
    from utils.cli_arg_validators import *
import argparse
from re import T
import runpy
import json
from datetime import datetime
import ast

class About:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "build_metadata.json"), "r") as f:
            build_metadata = json.loads(f.read())
            self._info = {
                "name": "Typethon",
                "version": runpy.run_path(
                    os.path.join(os.path.dirname(__file__), "__version__.py")
                )["__version__"],
                "author": "obfuscatedgenerated",
                "license": "MIT",
                "contributors": build_metadata["contributors"],
                "build_timestamp": build_metadata["build_timestamp"],
                "build_commit": build_metadata["build_commit"],
                "build_commit_short": build_metadata["build_commit_short"],
            }

    def get(self, key):
        return self._info[key]

    def get_all(self):
        return self._info

    def get_basic(self):
        return self._info["name"] + " " + self._info["version"] + " (" + self._info["build_commit_short"] + ") by " + self._info["author"] + " under " + self._info["license"] + " - Built on " + datetime.fromtimestamp(self._info["build_timestamp"]).strftime("%d %b %Y at %H:%M:%S")

class Visitor(ast.NodeVisitor):
    level = 0
    func_decs = {}
    func_anns = {}
    func_anns_returns = {}
    clean_decorators = {}
    def generic_visit(self, node):
        self.level += 1
        if isinstance(node, ast.FunctionDef):
            self.func_decs[node.name] = node.decorator_list
            self.func_anns[node.name] = {}
            for arg in node.args.args:
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        self.func_anns[node.name][arg.arg] = arg.annotation.id # convert this to class/type by its name
                    elif isinstance(arg.annotation, ast.Constant):
                        self.func_anns[node.name][arg.arg] = arg.annotation.value # this is already a class/type
            for arg in node.args.kwonlyargs:
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        self.func_anns[node.name][arg.arg] = arg.annotation.id # convert this to class/type by its name
                    elif isinstance(arg.annotation, ast.Constant):
                        self.func_anns[node.name][arg.arg] = arg.annotation.value # this is already a class/type
            for arg in node.args.posonlyargs:
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        self.func_anns[node.name][arg.arg] = arg.annotation.id # convert this to class/type by its name
                    elif isinstance(arg.annotation, ast.Constant):
                        self.func_anns[node.name][arg.arg] = arg.annotation.value # this is already a class/type
            if node.returns:
                # need to support @Strict
                if isinstance(node.returns, ast.Name):
                    self.func_anns_returns[node.name] = node.returns.id # convert this to class/type by its name
                elif isinstance(node.returns, ast.Constant):
                    self.func_anns_returns[node.name] = node.returns.value # this is already a class/type

        #print(f'{"    "*self.level}entering {ast.dump(node)}')
        super().generic_visit(node)
        self.level -= 1
        #print(f'{"    "*self.level}leaving {ast.dump(node)}')
    
    def generate_clean_decorators(self):
        # need to support @Strict
        for func in self.func_decs:
            self.clean_decorators[func] = {}
            for dec in self.func_decs[func]:
                if isinstance(dec, ast.Name):
                    print(ast.dump(dec))
                    print("expect a crash, need to treat strict as a combination of the 2 decorators")
                # if @Strict is used, it should be name (current implementation)
                # once @Strict implements arguments, it will be a func as per the other decorators
                if not dec.func.id in self.clean_decorators[func]:
                    self.clean_decorators[func][dec.func.id] = {}
                for kwd in dec.keywords:
                    self.clean_decorators[func][dec.func.id][kwd.arg] = ast.unparse(kwd.value)
    
    def merge_annotations_to_types(self):
        # need to support @Strict
        for func in self.clean_decorators:
            for dec in self.clean_decorators[func]:
                if not "use_annotations" in self.clean_decorators[func][dec]:
                    continue
                if self.clean_decorators[func][dec]["use_annotations"]:
                    if dec == "ArgumentTypes":
                        if "types" in self.clean_decorators[func][dec]:
                            for type_key in self.func_anns[func]:
                                if type_key in self.func_anns[func]:
                                    self.clean_decorators[func][dec]["types"][type_key] = self.func_anns[func][type_key]
                        else:
                            self.clean_decorators[func][dec]["types"] = self.func_anns[func].copy()
                    elif dec == "ReturnType":
                        self.clean_decorators[func][dec]["types"] = self.func_anns_returns[func]
    
    def get_return_type_of_func(self, func):
        # need to support @Strict
        if "ReturnType" in self.clean_decorators[func]:
            if "types" in self.clean_decorators[func]["ReturnType"]:
                types = self.clean_decorators[func]["ReturnType"]["types"]
                if isinstance(types, type(None)):
                    return type(None)
    
    def get_return_constraints_of_func(self, func):
        # need to support @Strict
        if "ReturnType" in self.clean_decorators[func]:
            if "constraints" in self.clean_decorators[func]["ReturnType"]:
                return self.clean_decorators[func]["ReturnType"]["constraints"]
    
    def get_arg_types_of_func(self, func):
        # need to support @Strict
        if "ArgumentTypes" in self.clean_decorators[func]:
            if "types" in self.clean_decorators[func]["ArgumentTypes"]:
                return self.clean_decorators[func]["ArgumentTypes"]["types"]
    
    def get_arg_constraints_of_func(self, func):
        # need to support @Strict
        if "ArgumentTypes" in self.clean_decorators[func]:
            if "constraints" in self.clean_decorators[func]["ArgumentTypes"]:
                return self.clean_decorators[func]["ArgumentTypes"]["constraints"]

def main():
    top_ap = argparse.ArgumentParser(description="The Typethon CLI.")
    top_ap.add_argument("-j", "--json", action="store_true", help="Print in JSON for programmatic use.")
    sub_aps = top_ap.add_subparsers(required=True, dest="command")

    about_ap = sub_aps.add_parser(
        "about",
        help="Get information about the installed Typethon version.",
        description="Get information about the installed Typethon version.",
    )
    about_ap.add_argument(
        "-g", "--get", metavar="KEY", help="Get a a property from the information."
    )

    lint_ap = sub_aps.add_parser(
        "lint",
        help="Lint a .py file for type errors.",
        description="Lint a .py file for type errors.",
    )
    lint_ap.add_argument(
        "input_file", help="The .py file to lint.", type=file_path, metavar="PATH"
    )
    
    args = top_ap.parse_args()

    if args.command == "about":
        about = About()
        if args.get:
            print(about.get(args.get))
        elif args.json:
            print(about.get_all())
        else:
            print(about.get_basic())
    elif args.command == "lint":
        with open(args.input_file, "r") as f:
            code = f.read()
        tree = ast.parse(code)
        visitor = Visitor()
        visitor.visit(tree)
        #print(visitor.func_anns)
        visitor.generate_clean_decorators()
        #print(visitor.clean_decorators)
        visitor.merge_annotations_to_types()
        for func in visitor.clean_decorators:
            print(f"{func}:")
            print(f"    Return Type: {visitor.get_return_type_of_func(func)}")
            print(f"    Return Constraints: {visitor.get_return_constraints_of_func(func)}")
            print(f"    Argument Types: {visitor.get_arg_types_of_func(func)}")
            print(f"    Argument Constraints: {visitor.get_arg_constraints_of_func(func)}")
        #print(ast.dump(tree, indent=4))


if __name__ == "__main__":
    main()