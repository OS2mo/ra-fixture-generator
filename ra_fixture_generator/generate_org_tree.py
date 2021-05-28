#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import Tuple
from typing import TypeVar

from mimesis import Address


OrgTree = Dict[str, Dict]


def generate_cantina() -> OrgTree:
    if random.random() > 0.5:
        return {"Kantine": {}}
    return {}


def gen_schools_and_childcare(
    seed: str, num_schools: int = 30, num_childcare: int = 20
) -> OrgTree:
    address_gen = Address("da", seed=seed)

    def generate_school(_: int) -> Tuple[str, OrgTree]:
        name = address_gen.city() + " skole"
        return name, {}

    def generate_childcare(_: int) -> Tuple[str, OrgTree]:
        name = address_gen.city() + " børnehus"
        if random.random() > 0.5:
            return name, {"Administration": {}}
        if random.random() > 0.5:
            return name, {"Teknisk Support": {}}
        return name, {}

    ret = {}
    ret.update(dict(map(generate_school, range(num_schools))))
    ret.update(dict(map(generate_childcare, range(num_childcare))))
    return ret


def gen_org_tree(seed: str) -> OrgTree:
    random.seed(seed)
    return {
        "Borgmesterens Afdeling": {
            "Budget og Planlægning": {},
            "HR og organisation": {},
            "Erhverv": {},
            "Byudvikling": {},
            "IT-Support": {},
        },
        "Teknik og Miljø": {
            "Kloakering": generate_cantina(),
            "Park og vej": generate_cantina(),
            "Renovation": generate_cantina(),
            "Belysning": generate_cantina(),
            "IT-Support": generate_cantina(),
        },
        "Skole og Børn": {
            "Social Indsats": {
                "Skole og børnehaver": gen_schools_and_childcare(seed),
            },
            "IT-Support": generate_cantina(),
        },
        "Social og sundhed": {},
    }


CallableReturnType = TypeVar("CallableReturnType")


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


if __name__ == "__main__":
    random_seed = "0xFF"
    org_tree = gen_org_tree(random_seed)
    print(org_tree)

    def yield_func(name: str, level: int, prefix: str) -> str:
        return "  " * (level - 1) + name

    for string in list(tree_visitor(org_tree, yield_func)):
        print(string)

    for string in list(tree_visitor_levels(org_tree, yield_func)):
        print(string)
