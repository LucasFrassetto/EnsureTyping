# build-in imports
from typing import List, Union


__all__ = ("ensure_typing")


def ensure_typing(var, var_name: str, types: Union[List[type], type], optional: bool=False):
    """_summary_

    Args:
        var (_type_): _description_
        var_name (str): _description_
        types (Union[List[type], type]): _description_
        optional (bool, optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    if not isinstance(types, list):
        types = [types]
    if optional and var == None:
        return True

    if not optional and var == None:
        raise ValueError(f"This parameter is mandatory, please enter a valid value. - {var_name}:[{types}]{var}")

    for type_ in types:
        if type_ == types[-1] and not isinstance(var, type_):
            raise TypeError(f"Please enter a valid value to {var_name}. {var_name}{types}: {var}{type(var)}")
        break
