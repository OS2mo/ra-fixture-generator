# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from functools import partial
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo.details import Address

from .base import BaseGenerator
from ..util import EmployeeValidity


class EmployeeAddressGenerator(BaseGenerator):
    def __init__(self, employee_address_types: dict[str, UUID]) -> None:
        super().__init__()
        self.employee_address_types = employee_address_types
        self.person_gen = Person("da")

    @staticmethod
    def gen_building() -> str:
        return "Bygning {}".format(random.randrange(1, 20))

    def generate(self, employees: list[Employee]) -> list[Address]:
        generators = [
            # TODO: dar_uuid needs to be valid, fetch from DAR?
            # (generate_uuid("fake-dar-1" + str(employee_uuid)),
            #  generate_uuid("AdressePostEmployee")),
            (self.person_gen.email, self.employee_address_types["EmailEmployee"]),
            (
                partial(self.person_gen.telephone, "########"),
                self.employee_address_types["PhoneEmployee"],
            ),
            (self.gen_building, self.employee_address_types["LocationEmployee"]),
        ]

        def construct_addresses(employee: Employee) -> list[Address]:

            return [
                Address.from_simplified_fields(
                    value=str(generator()),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    person_uuid=employee.uuid,
                    **self.random_validity(EmployeeValidity).dict(),
                )
                for generator, address_type_uuid in random.choices(
                    generators, k=int(random.gammavariate(alpha=5, beta=0.6))
                )
            ]

        return list(more_itertools.flatten(map(construct_addresses, employees)))
