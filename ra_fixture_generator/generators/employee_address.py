# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import List

import more_itertools
from mimesis import Person
from ramodels.lora import Organisation
from ramodels.mo import Employee
from ramodels.mo.details import Address

from .base import BaseGenerator


class EmployeeAddressGenerator(BaseGenerator):
    def __init__(self, seed: str = None) -> None:
        super().__init__(seed)
        self.person_gen = Person("da", seed=seed)

    def generate(
        self, organisation: Organisation, employees: List[Employee]
    ) -> List[Address]:
        def construct_addresses(employee: Employee) -> List[Address]:
            employee_uuid = employee.uuid

            addresses = [
                # TODO: dar_uuid needs to be valid, fetch from DAR?
                # (generate_uuid("fake-dar-1" + str(employee_uuid)),
                #  generate_uuid("AdressePostEmployee")),
                (self.person_gen.email(), self.generate_uuid("EmailEmployee")),
                (
                    self.person_gen.telephone("########"),
                    self.generate_uuid("PhoneEmployee"),
                ),
                (
                    "Bygning {}".format(random.randrange(1, 20)),
                    self.generate_uuid("LocationEmployee"),
                ),
            ]

            return [
                Address.from_simplified_fields(
                    uuid=self.generate_uuid(str(employee_uuid) + str(value)),
                    value=str(value),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    org_uuid=organisation.uuid,
                    from_date="1930-01-01",  # todo: ensure this isn't before the associated org_unit or person
                    person_uuid=employee_uuid,
                )
                for value, address_type_uuid in addresses
            ]

        return list(more_itertools.flatten(map(construct_addresses, employees)))
