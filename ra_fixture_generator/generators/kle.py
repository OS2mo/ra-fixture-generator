# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from ramodels.mo import OrganisationUnit
from ramodels.mo._shared import KLEAspectRef
from ramodels.mo._shared import KLENumberRef
from ramodels.mo._shared import OrgUnitRef
from ramodels.mo.details import KLE

from .base import BaseGenerator


class KLEGenerator(BaseGenerator):
    def __init__(
        self,
        kle_aspects: dict[str, UUID],
        kle_numbers: dict[str, UUID],
    ) -> None:
        super().__init__()
        self.kle_aspect_uuids = list(kle_aspects.values())
        self.kle_number_uuids = list(kle_numbers.values())

    def generate(self, org_layers: list[list[OrganisationUnit]]) -> list[list[KLE]]:
        print("Generating organisation KLEs")
        kle_aspect_refs = [KLEAspectRef(uuid=uuid) for uuid in self.kle_aspect_uuids]

        def construct_kles(org_unit: OrganisationUnit) -> list[KLE]:
            return [
                KLE(
                    kle_number=KLENumberRef(uuid=kle_number_uuid),
                    kle_aspect=random.sample(
                        kle_aspect_refs,
                        k=random.randint(1, len(self.kle_aspect_uuids)),
                    ),
                    org_unit=OrgUnitRef(uuid=org_unit.uuid),
                    validity=self.random_validity(org_unit.validity),
                )
                for kle_number_uuid in random.sample(
                    self.kle_number_uuids,
                    k=int(random.gammavariate(alpha=4, beta=0.5)),
                )
            ]

        return [
            list(more_itertools.flatten(map(construct_kles, layer)))
            for layer in org_layers
        ]
