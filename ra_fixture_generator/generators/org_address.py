# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import List

import more_itertools
from mimesis import Code
from mimesis import Internet
from mimesis import Person
from mimesis.enums import EANFormat
from ramodels.lora import Organisation
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address

from ..util import PNummer
from .base import BaseGenerator


class OrgAddressGenerator(BaseGenerator):
    def __init__(self, seed: str = None) -> None:
        super().__init__(seed)
        self.code_gen = Code(seed=seed)
        self.internet_gen = Internet(seed=seed)
        self.person_gen = Person("da", seed=seed)
        self.pnummer_gen = PNummer(seed=seed)

    def generate(
        self, organisation: Organisation, org_layers: List[List[OrganisationUnit]]
    ) -> List[List[Address]]:
        def construct_addresses(org_unit: OrganisationUnit) -> List[Address]:
            org_unit_uuid = org_unit.uuid

            addresses = [
                # TODO: dar_uuid needs to be valid, fetch from DAR?
                # (generate_uuid("fake-dar-1" + str(org_unit_uuid)),
                #  generate_uuid("AdresseMailUnit")),
                # (generate_uuid("fake-dar-2" + str(org_unit_uuid)),
                #  generate_uuid("AdresseHenvendelsessted")),
                # (generate_uuid("fake-dar-3" + str(org_unit_uuid)),
                #  generate_uuid("AdressePostRetur")),
                (self.person_gen.telephone("########"), self.generate_uuid("FaxUnit")),
                (
                    self.person_gen.telephone("########"),
                    self.generate_uuid("PhoneUnit"),
                ),
                (self.person_gen.email(), self.generate_uuid("EmailUnit")),
                (self.code_gen.ean(EANFormat.EAN13), self.generate_uuid("EAN")),
                (self.pnummer_gen.pnumber(), self.generate_uuid("p-nummer")),
                (
                    "Bygning {}".format(random.randrange(1, 20)),
                    self.generate_uuid("LocationUnit"),
                ),
                (self.internet_gen.url(), self.generate_uuid("WebUnit")),
            ]

            return [
                Address.from_simplified_fields(
                    uuid=self.generate_uuid(str(org_unit_uuid) + str(value)),
                    value=str(value),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    org_uuid=organisation.uuid,
                    from_date="1930-01-01",
                    org_unit_uuid=org_unit_uuid,
                )
                for value, address_type_uuid in addresses
            ]

        return [
            list(more_itertools.flatten(map(construct_addresses, layer)))
            for layer in org_layers
        ]
