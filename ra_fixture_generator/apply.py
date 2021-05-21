#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from functools import wraps
from inspect import signature as func_signature
from typing import Callable
from typing import Tuple
from typing import TypeVar

CallableReturnType = TypeVar("CallableReturnType")


def has_self_arg(func):
    """Return True if the given function has a 'self' argument."""
    args = list(func_signature(func).parameters)
    return args and args[0] in ("self", "cls")


def apply(func: Callable[..., CallableReturnType]) -> Callable[..., CallableReturnType]:
    """Decorator to apply tuple to function.

    Example:

        @apply
        async def dual(key, value):
            return value

        print(dual(('k', 'v')))  # --> 'v'

    Args:
        func (function): The function to apply arguments for.

    Returns:
        :obj:`sync function`: The function which has had it argument applied.
    """

    if has_self_arg(func):

        @wraps(func)
        def wrapper(self, tup: Tuple) -> CallableReturnType:
            return func(self, *tup)

    else:

        @wraps(func)
        def wrapper(tup: Tuple) -> CallableReturnType:
            return func(*tup)

    return wrapper
