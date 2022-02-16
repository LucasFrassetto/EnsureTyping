# build-in imports
import inspect
from dataclasses import dataclass

# project imports
import ensure_typing


__all__ = ("EnsureTyping")


@dataclass
class EnsureTyping:
    """This Decorator's function is to Force the Typing Check of a class or Function. raising exceptions if it is an invalid type or an invalid type value.

    Args:
        recursive_objects (bool): #? goes through all classes, subclasses, functions and subfunctions collecting all parameters and checking if the typing is correct. Defaults to False.
        recursive_variables (bool): #? goes through all classes, subclasses, functions and subfunctions collecting all variables and checking if the typing is correct. Defaults to False.
        ignore_exception (bool): #? Ignores exceptions and only raises a warning if the typing is incorrect.. Defaults to False.

    """
    # TODO Check object is class or function
    # TODO Check variables and class/function params

    recursive_objects: bool = False
    recursive_variables: bool = False
    ignore_exception: bool = False

    def __post_init__(self):
        ensure_typing(self.recursive, "recursive", bool, True)
        ensure_typing(self.ignore_exception, "ignore_exception", bool, True)

    def __call__(self, obj, *args, **kwargs):
        def inner(*args, **kwargs):
            func_params = dict(inspect.signature(obj).parameters)
            args_params = {param:args[e] if e <= len(args)-1 else None for e, param in enumerate(func_params)}

            for param, _type in func_params.items():
                optional = _type.default != _type.empty
                default_value = _type.default if optional else None

                func_params[param] = {'type': _type.annotation, 'value': None, 'default_value': default_value, 'optional': optional}

            if args_params:
                for arg, value in args_params.items():
                    func_params[arg]['value'] = value

            if kwargs:
                for kw, value in kwargs.items():
                    func_params[kw]['value'] = value

            for param, item in func_params.items():
                ensure_typing(item['value'], param, item['type'], item['optional'])

            return obj(*args, **kwargs)
        return inner