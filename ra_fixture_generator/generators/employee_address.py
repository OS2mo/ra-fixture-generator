# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo.details import Address

from .base import BaseGenerator
from ..util import EmployeeValidity


class EmployeeAddressGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.person_gen = Person("da")

    def generate(
        self, employees: list[Employee], employee_address_types: dict[str, UUID]
    ) -> list[Address]:
        email_uuid = employee_address_types["EmailEmployee"]
        phone_uuid = employee_address_types["PhoneEmployee"]
        location_uuid = employee_address_types["LocationEmployee"]

        def construct_addresses(employee: Employee) -> list[Address]:
            addresses = [
                # TODO: dar_uuid needs to be valid, fetch from DAR?
                # (generate_uuid("fake-dar-1" + str(employee_uuid)),
                #  generate_uuid("AdressePostEmployee")),
                (self.person_gen.email(), email_uuid),
                (self.person_gen.telephone("########"), phone_uuid),
                ("Bygning {}".format(random.randrange(1, 20)), location_uuid),
            ]

            return [
                Address.from_simplified_fields(
                    value=str(value),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    person_uuid=employee.uuid,
                    **self.random_validity(EmployeeValidity).dict(),
                )
                for value, address_type_uuid in addresses
            ]

        return list(more_itertools.flatten(map(construct_addresses, employees)))
