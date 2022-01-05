# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections import Callable
from typing import Dict
from typing import Iterator
from typing import TypeVar

from mimesis.builtins.base import BaseSpecProvider


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
OrgTree = Dict[str, Dict]


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
