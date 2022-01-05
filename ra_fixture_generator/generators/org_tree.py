# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import Tuple

from mimesis import Address
from mimesis import Development

from ..util import OrgTree
from .base import BaseGenerator


class OrgTreeGenerator(BaseGenerator):
    def __init__(self, seed: str = None) -> None:
        super().__init__(seed)
        self.address_gen = Address("da", seed=seed)
        self.development_gen = Development(seed=seed)

    def generate(self, size: int) -> OrgTree:
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
                        num_technical_support=size // 10,
                    ),
                },
                "IT-Support": self.generate_cantina(),
            },
            "Social og sundhed": {},
        }

    def gen_schools_and_childcare(
        self,
        num_schools: int,
        num_childcare: int,
        num_technical_support: int,
    ) -> OrgTree:
        def generate_school() -> Tuple[str, OrgTree]:
            name = self.address_gen.city() + " skole"
            school = {}
            if random.random() > 0.5:
                school["Administration"] = {}
            if random.random() > 0.5:
                school["Teknisk Support"] = {
                    f"Teknisk support for {self.development_gen.os()}": {}
                    for _ in range(num_technical_support)
                }
            return name, {}

        def generate_childcare() -> Tuple[str, OrgTree]:
            name = self.address_gen.city() + " børnehave"
            return name, {}

        ret = {}
        ret.update(generate_school() for _ in range(num_schools))
        ret.update(generate_childcare() for _ in range(num_childcare))
        return ret

    def generate_cantina(self) -> OrgTree:
        if random.random() > 0.5:
            return {"Kantine": {}}
        return {}
