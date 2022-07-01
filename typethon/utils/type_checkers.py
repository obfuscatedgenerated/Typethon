def generic_arg_type_check(func, args, kwargs, types, constraints, use_annotations):
    if (
        func.__qualname__.split(".")[0] == "ReturnType"
        or func.__qualname__.split(".")[0] == "ArgumentTypes"
    ):
        if not "passedFuncName" in func.__dict__:
            func.__name__ = "a function originating from " + func.__name__
        else:
            func.__name__ = func.passedFuncName + "() originating from " + func.__name__

    if not "usePassedArgs" in func.__dict__:
        func.usePassedArgs = False

    if func.usePassedArgs:
        annotations = func.passedAnnotations
        co_argcount = func.passedCo_argcount
        co_varnames = func.passedCo_varnames
        defaults = func.passedDefaults
    else:
        annotations = func.__annotations__
        co_argcount = func.__code__.co_argcount
        co_varnames = func.__code__.co_varnames
        defaults = func.__defaults__

    arg_dict = kwargs.copy()

    all_args = co_argcount

    if defaults is not None:
        kwarg_count = len(defaults)
    else:
        kwarg_count = 0

    pos_args = all_args - kwarg_count

    if len(args) > pos_args:
        raise TypeError(
            f"{func.__name__}() takes {pos_args} positional arguments but {len(args)} were given"
        )

    if defaults is not None:
        defaults_map = dict(zip(co_varnames[-len(defaults) :], defaults))
    else:
        defaults_map = {}

    for i, arg in enumerate(args):
        arg_dict[co_varnames[i]] = arg

    for key in arg_dict:
        if key not in co_varnames:
            raise TypeError(
                f'argument "{key}" is not a valid argument for {func.__name__}() call'
            )

    for name in co_varnames:
        if name not in arg_dict:
            if name in defaults_map:
                arg_dict[name] = defaults_map[name]
            else:
                raise TypeError(
                    f'argument "{name}" is missing from {func.__name__}() call'
                )

    if use_annotations:
        for key, value in annotations.items():
            types[key] = value

    for key, value in types.items():
        if key == "return":
            continue
        if not isinstance(arg_dict[key], value):
            raise TypeError(
                f'argument "{key}" is not of type {types[key].__name__} in {func.__name__}() call, it is of type {type(arg_dict[key]).__name__} with value {arg_dict[key]}'
            )

    for key, value in constraints.items():
        if isinstance(value, tuple) or isinstance(value, list):
            for i, constraint in enumerate(value):
                if not constraint(arg_dict[key]):
                    raise TypeError(
                        f'argument "{key}" does not fit to constraint {constraints[key][i].__name__} (constraint index {i}) in {func.__name__}() call with value {arg_dict[key]}'
                    )
        else:
            if not value(arg_dict[key]):
                raise TypeError(
                    f'argument "{key}" does not fit to constraint {constraints[key].__name__} in {func.__name__}() call with value {arg_dict[key]}'
                )

    return func(**arg_dict)


def generic_return_type_check(func, args, kwargs, types, constraints, use_annotations):
    result = func(*args, **kwargs)
    if (
        func.__qualname__.split(".")[0] == "ReturnType"
        or func.__qualname__.split(".")[0] == "ArgumentTypes"
    ):
        if not "passedFuncName" in func.__dict__:
            func.__name__ = "a function originating from " + func.__name__
        else:
            func.__name__ = func.passedFuncName + "() originating from " + func.__name__

    if not "usePassedArgs" in func.__dict__:
        func.usePassedArgs = False

    if func.usePassedArgs:
        annotations = func.passedAnnotations
        co_argcount = func.passedCo_argcount
        co_varnames = func.passedCo_varnames
        defaults = func.passedDefaults
    else:
        annotations = func.__annotations__
        co_argcount = func.__code__.co_argcount
        co_varnames = func.__code__.co_varnames
        defaults = func.__defaults__

    if use_annotations:
        if "return" in annotations:
            if annotations.get("return") is None:
                types = type(None)
            else:
                types = annotations.get("return")

    if types is not None:
        if not isinstance(result, types):
            raise TypeError(
                f"return value is not of type {types.__name__} in {func.__name__}() call, it is of type {type(result).__name__} with value {result}"
            )

    if isinstance(constraints, tuple) or isinstance(constraints, list):
        for i, constraint in enumerate(constraints):
            if not constraint(result):
                raise TypeError(
                    f"return value does not fit to constraint {constraints[i].__name__} (constraint index {i}) in {func.__name__}() call with value {result}"
                )
    else:
        if not constraints(result):
            raise TypeError(
                f"return value does not fit to constraint {constraints.__name__} in {func.__name__}() call with value {result}"
            )
    return result
