# build-in imports
from typing import List, Union


__all__ = ("ensure_typing")


def ensure_typing(var, var_name: str, types: Union[List[type], type], optional: bool=False):
    """this function aims to ensure that the provided value matches valid types.

    Args:
        var (Any): variable whose typo will be checked.
        var_name (str): variable name for reference.
        types (Union[List[type], type]): a type or a list of types that "var" can be.
        optional (bool, optional): if this variable is optional.. Defaults to False.

    Raises:
        ValueError: raises an exception if the variable is not optional and is empty.
        TypeError: raises an exception if the value type is different from the correct type
    """
    if not isinstance(types, list):
        types = [types]

    for type_ in types:
        if type_ == types[-1] and not isinstance(var, type_):
            if not optional and type_ != type(None) and not var:
                raise ValueError(f"This parameter is mandatory, please enter a valid value. - {var_name}{types}: {var}{type(var)}")
            raise TypeError(f"Please enter a valid value to {var_name}. {var_name}{types}: {var}{type(var)}")
        break
