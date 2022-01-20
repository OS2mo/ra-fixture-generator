# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from collections.abc import Iterator
from functools import cached_property
from functools import partial
from typing import Callable
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo.details import Address

from ..util import EmployeeValidity
from ..util import thawed
from .base import BaseGenerator


class EmployeeAddressGenerator(BaseGenerator):
    def __init__(self, employee_address_types: dict[str, UUID]) -> None:
        super().__init__()
        self.employee_address_types = employee_address_types
        self.person_gen = Person("da")

    @staticmethod
    def gen_building() -> str:
        return "Bygning {}".format(random.randrange(1, 20))

    @cached_property
    def generators(self) -> dict[UUID, Callable]:
        return {
            # TODO: dar_uuid needs to be valid, fetch from DAR?
            # (generate_uuid("fake-dar-1" + str(employee_uuid)),
            #  generate_uuid("AdressePostEmployee")),
            self.employee_address_types["EmailEmployee"]: self.person_gen.email,
            self.employee_address_types["PhoneEmployee"]: partial(
                self.person_gen.telephone, "########"
            ),
            self.employee_address_types["LocationEmployee"]: self.gen_building,
        }

    def generate(self, employees: list[Employee]) -> list[Address]:
        def construct_addresses(employee: Employee) -> list[Address]:
            return [
                Address.from_simplified_fields(
                    value=str(generator()),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    person_uuid=employee.uuid,
                    **self.random_validity(EmployeeValidity).dict(),
                )
                for address_type_uuid, generator in random.choices(
                    list(self.generators.items()),
                    k=int(random.gammavariate(alpha=5, beta=0.6)),
                )
            ]

        return list(more_itertools.flatten(map(construct_addresses, employees)))

    def generate_modifications(self, addresses: list[Address]) -> list[Address]:
        def construct_modification(address: Address) -> Iterator[Address]:
            while random.random() < 0.2:
                with thawed(address.copy()) as copy:
                    copy.value = self.generators[address.address_type.uuid]()
                    copy.validity = self.random_validity(EmployeeValidity)
                yield copy

        return list(more_itertools.flatten(map(construct_modification, addresses)))
