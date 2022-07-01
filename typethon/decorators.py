from .utils import type_checkers as tc


class ArgumentTypes:
    def __init__(
        self,
        overflow_func=None,
        types={},
        constraints={},
        use_annotations=False,
        use_arg_passing=True,
    ):
        self.types = types.copy()
        self.constraints = constraints.copy()
        self.use_annotations = use_annotations
        self.use_arg_passing = use_arg_passing
        if overflow_func is not None:
            raise SyntaxError("this decorator must be called as a function")

    def __call__(self, func=None):
        def argTypesWrapper(*args, **kwargs):
            return tc.generic_arg_type_check(
                func,
                args,
                kwargs,
                self.types,
                self.constraints,
                self.use_annotations,
            )

        argTypesWrapper.passedAnnotations = func.__annotations__
        argTypesWrapper.passedCo_varnames = func.__code__.co_varnames
        argTypesWrapper.passedCo_argcount = func.__code__.co_argcount
        argTypesWrapper.passedDefaults = func.__defaults__
        argTypesWrapper.usePassedArgs = self.use_arg_passing
        argTypesWrapper.passedFuncName = func.__name__
        return argTypesWrapper


class ReturnType:
    def __init__(
        self,
        overflow_func=None,
        types=None,
        constraints=(),
        use_annotations=False,
        use_arg_passing=True,
    ):
        self.types = types
        self.constraints = constraints
        self.use_annotations = use_annotations
        self.use_arg_passing = use_arg_passing
        if overflow_func is not None:
            raise SyntaxError("this decorator must be called as a function")

    def __call__(self, func):
        def returnTypeWrapper(*args, **kwargs):
            return tc.generic_return_type_check(
                func,
                args,
                kwargs,
                self.types,
                self.constraints,
                self.use_annotations,
            )

        returnTypeWrapper.passedAnnotations = func.__annotations__
        returnTypeWrapper.passedCo_varnames = func.__code__.co_varnames
        returnTypeWrapper.passedCo_argcount = func.__code__.co_argcount
        returnTypeWrapper.passedDefaults = func.__defaults__
        returnTypeWrapper.usePassedArgs = self.use_arg_passing
        returnTypeWrapper.passedFuncName = func.__name__
        return returnTypeWrapper

class Strict:
    def __init__(self, overflow_func=None, arg_constraints={}, return_constraints=()):
        if overflow_func is not None:
            raise SyntaxError("this decorator must be called as a function")
        self.arg_constraints = arg_constraints
        self.return_constraints = return_constraints
    def __call__(self, func):
        def strictWrapper(*args, **kwargs):
            return ArgumentTypes(use_annotations=True, constraints=self.arg_constraints)(ReturnType(use_annotations=True, constraints=self.return_constraints)(func))(*args, **kwargs)
        strictWrapper.passedAnnotations = func.__annotations__
        strictWrapper.passedCo_varnames = func.__code__.co_varnames
        return strictWrapper