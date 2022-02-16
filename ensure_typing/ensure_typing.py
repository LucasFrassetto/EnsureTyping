# build-in imports
import logging
from inspect import _empty, signature
from dataclasses import dataclass
from typing import List, Union, _UnionGenericAlias

# project imports
import ensure_typing


__all__ = ("EnsureTyping", "ensure_typing")


def _raise(text, error, ignore):
    if not ignore:
        raise error(text)
    else:
        logging.warning(text)


def ensure_typing(var, var_name: str, types: Union[List[type], type], optional: bool=False, ignore_exception:bool=False):
    """this function aims to ensure that the provided value matches valid types.

    Args:
        var (Any): variable whose typo will be checked.
        var_name (str): variable name for reference.
        types (Union[List[type], type]): a type or a list of types that "var" can be.
        optional (bool, optional): if this variable is optional.. Defaults to False.
        ignore_exception (bool, optional): Ignores exceptions and only raises a warning if the typing is incorrect. Defaults to False.

    Raises:
        ValueError: raises an exception if the variable is not optional and is empty.
        TypeError: raises an exception if the type is invalid.
        TypeError: raises an exception if the value type is different from the correct type
    """
    types_ = ()
    if not isinstance(types, (list, tuple)) and type(types) != _UnionGenericAlias:
        types_ += (types,)
    elif isinstance(types, list):
        types_ += tuple(types)
    elif isinstance(types, _UnionGenericAlias):
        types_ += types.__args__

    if not types_:
        types_ = (_empty,)

    # check invalid types
    for type_ in types_:
        if type(type_) != type:
            _raise(f"Please enter a valid type to {types_}. ", TypeError, ignore_exception)

    if not isinstance(var, types_):
        if optional: pass
        elif _empty in types_: pass
        else:
            extra_msg = f"{var_name}{types_}: {var}{type(var)}"
            if not var and not optional:
                _raise(f"This parameter is mandatory, please enter a valid value. {extra_msg}", ValueError, ignore_exception)
            _raise(f"Please enter a valid value to {var_name}. {extra_msg}", TypeError, ignore_exception)


@dataclass
class EnsureTyping:
    """This Decorator's function is to Force the Typing Check of a class or Function. raising exceptions if it is an invalid type or an invalid type value.

    Args:
        recursive_objects (bool, optional): Goes through all classes, subclasses, functions and subfunctions collecting all parameters and checking if the typing is correct. Defaults to False.
        recursive_variables (bool, optional): Goes through all classes, subclasses, functions and subfunctions collecting all variables and checking if the typing is correct. Defaults to False.
        ignore_exception (bool, optional): Ignores exceptions and only raises a warning if the typing is incorrect.. Defaults to False.

    """
    # TODO Check object is class or function
    # TODO Check variables and class/function params

    recursive_objects: bool = False
    recursive_variables: bool = False
    ignore_exception: bool = False

    def __post_init__(self):
        ensure_typing(self.recursive_objects, "recursive_objects", bool, True)
        ensure_typing(self.recursive_variables, "recursive_variables", bool, True)
        ensure_typing(self.ignore_exception, "ignore_exception", bool, True)

    def __call__(self, obj, *args, **kwargs):
        def inner(*args, **kwargs):
            func_params = dict(signature(obj).parameters)
            args_params = {param:args[e] if e <= len(args)-1 else None for e, param in enumerate(func_params)}
            for param, _type in func_params.items():
                optional = _type.default != _empty
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
