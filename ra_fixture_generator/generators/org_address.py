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
from mimesis import Code
from mimesis import Internet
from mimesis import Person
from mimesis.enums import EANFormat
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address

from ..util import PNummer
from .base import BaseGenerator
from ..util import thawed


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

    @cached_property
    def generators(self) -> dict[UUID, Callable]:
        return {
            # TODO: dar_uuid needs to be valid, fetch from DAR?
            # (generate_uuid("fake-dar-1" + str(org_unit_uuid)),
            #  generate_uuid("AdresseMailUnit")),
            # (generate_uuid("fake-dar-2" + str(org_unit_uuid)),
            #  generate_uuid("AdresseHenvendelsessted")),
            # (generate_uuid("fake-dar-3" + str(org_unit_uuid)),
            #  generate_uuid("AdressePostRetur")),
            self.org_unit_address_types["FaxUnit"]: partial(
                self.person_gen.telephone, "########"
            ),
            self.org_unit_address_types["PhoneUnit"]: partial(
                self.person_gen.telephone, "########"
            ),
            self.org_unit_address_types["EmailUnit"]: self.person_gen.email,
            self.org_unit_address_types["EAN"]: partial(
                self.code_gen.ean, EANFormat.EAN13
            ),
            self.org_unit_address_types["p-nummer"]: self.pnummer_gen.pnumber,
            self.org_unit_address_types["LocationUnit"]: self.gen_building,
            self.org_unit_address_types["WebUnit"]: self.internet_gen.url,
        }

    def generate(self, org_layers: list[list[OrganisationUnit]]) -> list[list[Address]]:
        def construct_addresses(org_unit: OrganisationUnit) -> list[Address]:
            return [
                Address.from_simplified_fields(
                    value=str(generator()),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    org_unit_uuid=org_unit.uuid,
                    **self.random_validity(org_unit.validity).dict()
                )
                for address_type_uuid, generator in random.choices(
                    list(self.generators.items()),
                    k=int(random.gammavariate(alpha=7, beta=1)),
                )
            ]

        return [
            list(more_itertools.flatten(map(construct_addresses, layer)))
            for layer in org_layers
        ]

    def generate_modifications(
        self,
        address_layers: list[list[Address]],
        org_layers: list[list[OrganisationUnit]],
    ) -> list[Address]:
        org_unit_validities = {
            ou.uuid: ou.validity for ou in more_itertools.flatten(org_layers)
        }

        def construct_modification(address: Address) -> Iterator[Address]:
            while random.random() < 0.15:
                with thawed(address.copy()) as copy:
                    copy.value = self.generators[address.address_type.uuid]()
                    copy.validity = self.random_validity(
                        org_unit_validities[copy.org_unit.uuid]
                    )
                yield copy

        return list(
            more_itertools.flatten(
                map(construct_modification, more_itertools.flatten(address_layers))
            )
        )
