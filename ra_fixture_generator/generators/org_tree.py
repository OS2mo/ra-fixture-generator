# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import itertools
import random

from mimesis import Address
from mimesis import Development

from ..util import OrgTree
from .base import BaseGenerator


class OrgTreeGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.address_gen = Address("da")
        self.development_gen = Development()

    def generate(self, size: int) -> OrgTree:
        print("Generating organisation tree")

        return {
            "Borgmesterens Afdeling": {
                "Budget og Planlægning": {},
                "HR og organisation": {},
                "Erhverv": {},
                "Byudvikling": {},
                "IT-Support": {},
            },
            "Teknik og Miljø": {
                "Kloakering": self.generate_cantina(),
                "Park og vej": self.generate_cantina(),
                "Renovation": self.generate_cantina(),
                "Belysning": self.generate_cantina(),
                "IT-Support": self.generate_cantina(),
            },
            "Skole og Børn": {
                "Social Indsats": {
                    "Skoler og børnehaver": self.gen_schools_and_childcare(
                        num_schools=size * 6,
                        num_childcare=size * 4,
                    ),
                },
                "IT-Support": self.generate_cantina(),
            },
            "Social og sundhed": {},
        }

    def gen_schools_and_childcare(
        self, num_schools: int, num_childcare: int
    ) -> OrgTree:
        def generate_school() -> tuple[str, OrgTree]:
            name = f"{self.address_gen.postal_code()} - {self.address_gen.city()} skole"
            school = {}
            if random.random() > 0.5:
                school["Administration"] = {}
            school["Teknisk Support"] = {
                f"Teknisk support for {self.development_gen.os()}": {}
                for _ in range(int(random.gammavariate(alpha=2, beta=1)))
            }
            return name, school

        def generate_childcare() -> tuple[str, OrgTree]:
            name = self.address_gen.city() + " børnehave"
            return name, {}

        schools = (generate_school() for _ in range(num_schools))
        childcares = (generate_childcare() for _ in range(num_childcare))
        return dict(itertools.chain(schools, childcares))

    @staticmethod
    def generate_cantina() -> OrgTree:
        if random.random() > 0.5:
            return {"Kantine": {}}
        return {}
