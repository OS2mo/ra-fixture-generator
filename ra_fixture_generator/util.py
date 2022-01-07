# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections import Callable
from collections.abc import Iterator
from typing import Any
from typing import cast
from typing import TypeVar

import click
from mimesis.builtins.base import BaseSpecProvider
from pydantic import AnyHttpUrl
from pydantic import parse_obj_as
from pydantic import ValidationError


def validate_url(ctx: click.Context, param: Any, value: Any) -> AnyHttpUrl:
    try:
        return cast(AnyHttpUrl, parse_obj_as(AnyHttpUrl, value))
    except ValidationError as e:
        raise click.BadParameter(str(e))


class PNummer(BaseSpecProvider):
    class Meta:
        name = "pnummer"

    def _gen_x_digit_number(self, n: int) -> str:
        assert n > 0
        number = self.random.randint(0, 10 ** n - 1)
        return str(number).zfill(n)

    def pnumber(self) -> str:
        return self._gen_x_digit_number(10)


CallableReturnType = TypeVar("CallableReturnType")
OrgTree = dict[str, dict]


def tree_visitor(
    tree: OrgTree,
    yield_func: Callable[[str, int, str], CallableReturnType],
    level: int = 1,
    prefix: str = "",
) -> Iterator[CallableReturnType]:
    for name, children in tree.items():
        yield yield_func(name, level, prefix)
        yield from tree_visitor(children, yield_func, level + 1, prefix + name)


def tree_visitor_levels(
    tree: OrgTree,
    yield_func: Callable[[str, int, str], CallableReturnType],
    level: int = 1,
    prefix: str = "",
) -> Iterator[CallableReturnType]:
    for name, children in tree.items():
        yield yield_func(name, level, prefix)
    for name, children in tree.items():
        yield from tree_visitor_levels(children, yield_func, level + 1, prefix + name)
