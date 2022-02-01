# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from collections.abc import Iterator
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo.details import ITUser

from ..util import EmployeeValidity
from ..util import thawed
from .base import BaseGenerator


class ITUserGenerator(BaseGenerator):
    def __init__(self, it_systems: dict[str, UUID]) -> None:
        super().__init__()
        self.it_systems_uuids = list(it_systems.values())
        self.person_gen = Person("da")

    def generate(self, employees: list[Employee]) -> list[ITUser]:
        print("Generating employees")

        def construct_it_users(employee: Employee) -> list[ITUser]:
            return [
                ITUser.from_simplified_fields(
                    user_key=self.person_gen.username(mask="ld"),
                    itsystem_uuid=it_system_uuid,
                    person_uuid=employee.uuid,
                    **self.random_validity(EmployeeValidity).dict(),
                )
                for it_system_uuid in self.it_systems_uuids * 2
                if random.random() < 0.6
            ]

        return list(more_itertools.flatten(map(construct_it_users, employees)))

    def generate_modifications(self, it_users: list[ITUser]) -> list[ITUser]:
        def construct_modification(it_user: ITUser) -> Iterator[ITUser]:
            while random.random() < 0.35:
                with thawed(it_user.copy()) as copy:
                    copy.user_key = self.person_gen.username(mask="ld")
                    copy.validity = self.random_validity(EmployeeValidity)
                yield copy

        return list(more_itertools.flatten(map(construct_modification, it_users)))
