# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
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
    def __init__(self) -> None:
        super().__init__()
        self.code_gen = Code()
        self.internet_gen = Internet()
        self.person_gen = Person("da")
        self.pnummer_gen = PNummer()

    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        org_unit_address_types: dict[str, UUID],
    ) -> list[list[Address]]:
        fax_uuid = org_unit_address_types["FaxUnit"]
        phone_uuid = org_unit_address_types["PhoneUnit"]
        email_uuid = org_unit_address_types["EmailUnit"]
        ean_uuid = org_unit_address_types["EAN"]
        pnummer_uuid = org_unit_address_types["p-nummer"]
        location_uuid = org_unit_address_types["LocationUnit"]
        web_uuid = org_unit_address_types["WebUnit"]

        def construct_addresses(org_unit: OrganisationUnit) -> list[Address]:
            org_unit_uuid = org_unit.uuid

            addresses = [
                # TODO: dar_uuid needs to be valid, fetch from DAR?
                # (generate_uuid("fake-dar-1" + str(org_unit_uuid)),
                #  generate_uuid("AdresseMailUnit")),
                # (generate_uuid("fake-dar-2" + str(org_unit_uuid)),
                #  generate_uuid("AdresseHenvendelsessted")),
                # (generate_uuid("fake-dar-3" + str(org_unit_uuid)),
                #  generate_uuid("AdressePostRetur")),
                (self.person_gen.telephone("########"), fax_uuid),
                (self.person_gen.telephone("########"), phone_uuid),
                (self.person_gen.email(), email_uuid),
                (self.code_gen.ean(EANFormat.EAN13), ean_uuid),
                (self.pnummer_gen.pnumber(), pnummer_uuid),
                ("Bygning {}".format(random.randrange(1, 20)), location_uuid),
                (self.internet_gen.url(), web_uuid),
            ]

            return [
                Address.from_simplified_fields(
                    value=str(value),
                    value2=None,
                    address_type_uuid=address_type_uuid,
                    org_unit_uuid=org_unit_uuid,
                    **self.random_validity(org_unit.validity).dict()
                )
                for value, address_type_uuid in addresses
            ]

        return [
            list(more_itertools.flatten(map(construct_addresses, layer)))
            for layer in org_layers
        ]
