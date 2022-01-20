# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from datetime import date

import more_itertools
from mimesis import Person
from mimesis.enums import Gender
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit

from .base import BaseGenerator
from ..util import EmployeeValidity
from ..util import FixedDenmarkSpecProvider


class EmployeeGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.person_gen = Person("da")
        self.danish_gen = FixedDenmarkSpecProvider()

    def generate(
        self, org_layers: list[list[OrganisationUnit]], employees_per_org: int
    ) -> list[Employee]:
        num_orgs = more_itertools.ilen(more_itertools.flatten(org_layers))

        print("Number of organisation units:", num_orgs)
        print("Number of employees:", num_orgs * employees_per_org)
        cprs = set()

        def generate_employee(_: int) -> Employee:
            def even(x: int) -> bool:
                return (x % 2) == 0

            # Everyone's born between 60 and 30 years ago, so we can generate objects
            # associated with any employee without having to parse CPR back to a date.
            while True:
                cpr = self.danish_gen.cpr(
                    start=date.today().year - 60,
                    end=EmployeeValidity.from_date.year - 1,
                )
                if cpr not in cprs:
                    cprs.add(cpr)
                    break
            gender = Gender.MALE if even(int(cpr[-1])) else Gender.FEMALE

            return Employee(
                givenname=self.person_gen.name(gender=gender),
                surname=self.person_gen.surname(gender=gender),
                cpr_no=cpr,
            )

        return list(map(generate_employee, range(employees_per_org * num_orgs)))
