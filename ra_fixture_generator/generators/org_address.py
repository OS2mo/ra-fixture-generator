# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from functools import partial
from uuid import UUID

import more_itertools
from mimesis import Code
from mimesis import Internet
from mimesis import Person
from mimesis.enums import EANFormat
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address

from ..util import PNummer
from .base import BaseGenerator


class OrgAddressGenerator(BaseGenerator):
    def __init__(self, org_unit_address_types: dict[str, UUID]) -> None:
        super().__init__()
        self.org_unit_address_types = org_unit_address_types

        self.code_gen = Code()
        self.internet_gen = Internet()
        self.person_gen = Person("da")
        self.pnummer_gen = PNummer()

    @staticmethod
    def gen_building() -> str:
        return "Bygning {}".format(random.randrange(1, 20))

    def generate(self, org_layers: list[list[OrganisationUnit]]) -> list[list[Address]]:
        generators = [
            # TODO: dar_uuid needs to be valid, fetch from DAR?
            # (generate_uuid("fake-dar-1" + str(org_unit_uuid)),
            #  generate_uuid("AdresseMailUnit")),
            # (generate_uuid("fake-dar-2" + str(org_unit_uuid)),
            #  generate_uuid("AdresseHenvendelsessted")),
            # (generate_uuid("fake-dar-3" + str(org_unit_uuid)),
            #  generate_uuid("AdressePostRetur")),
            (
                partial(self.person_gen.telephone, "########"),
                self.org_unit_address_types["FaxUnit"],
            ),
            (
                partial(self.person_gen.telephone, "########"),
                self.org_unit_address_types["PhoneUnit"],
            ),
            (self.person_gen.email, self.org_unit_address_types["EmailUnit"]),
            (
                partial(self.code_gen.ean, EANFormat.EAN13),
                self.org_unit_address_types["EAN"],
            ),
            (self.pnummer_gen.pnumber, self.org_unit_address_types["p-nummer"]),
            (self.gen_building, self.org_unit_address_types["LocationUnit"]),
            (self.internet_gen.url, self.org_unit_address_types["WebUnit"]),
        ]

        def construct_addresses(org_unit: OrganisationUnit) -> list[Address]:
            org_unit_uuid = org_unit.uuid

            return [
                Address.from_simplified_fields(
                    value=str(generator()),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    org_unit_uuid=org_unit_uuid,
                    **self.random_validity(org_unit.validity).dict()
                )
                for generator, address_type_uuid in random.choices(
                    generators, k=int(random.gammavariate(alpha=7, beta=1))
                )
            ]

        return [
            list(more_itertools.flatten(map(construct_addresses, layer)))
            for layer in org_layers
        ]
